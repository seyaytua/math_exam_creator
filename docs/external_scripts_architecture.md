# External Scripts Feature - Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Math Exam Creator                       │
│                        (Main Application)                       │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────────┐
│                       Main Window                              │
│                   (src/main_window.py)                         │
├────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    Menu Bar                             │  │
│  │  ┌────────┬────────┬────────┬────────┬────────┬──────┐ │  │
│  │  │ File   │ Edit   │ Insert │ View   │ Tools  │ Help │ │  │
│  │  └────────┴────────┴────────┴────────┴───┬────┴──────┘ │  │
│  │                                           │              │  │
│  │                                           ▼              │  │
│  │                           ┌───────────────────────────┐ │  │
│  │                           │ Prompt Generator          │ │  │
│  │                           ├───────────────────────────┤ │  │
│  │                           │ ▶ Script 1 (Dynamic)      │ │  │
│  │                           │ ▶ Script 2 (Dynamic)      │ │  │
│  │                           │ ▶ Script 3 (Dynamic)      │ │  │
│  │                           ├───────────────────────────┤ │  │
│  │                           │ External Scripts Settings │ │  │
│  │                           ├───────────────────────────┤ │  │
│  │                           │ Print Settings            │ │  │
│  │                           └───────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────┬────────────────────────────────┬────────────────────┘
           │                                │
           │ User clicks                    │ User clicks
           │ "External Scripts Settings"    │ "▶ Script Name"
           │                                │
           ▼                                ▼
┌──────────────────────────┐    ┌────────────────────────────┐
│ ExternalScriptsDialog    │    │ execute_external_script()  │
│ (Configuration)          │    │ (Execution Handler)        │
├──────────────────────────┤    ├────────────────────────────┤
│                          │    │ 1. Validate paths          │
│ [Tab 1] [Tab 2] [Tab 3]  │    │ 2. Show confirmation       │
│                          │    │ 3. Execute subprocess      │
│ ┌─ Basic Info ─────────┐ │    │ 4. Capture output          │
│ │ Name: [___________]  │ │    │ 5. Show results            │
│ │ Desc: [___________]  │ │    └────────────┬───────────────┘
│ └──────────────────────┘ │                 │
│                          │                 │
│ ┌─ Python Env ─────────┐ │                 ▼
│ │ Path: [___][Browse]  │ │    ┌────────────────────────────┐
│ │ [Use Current Python] │ │    │ subprocess.run()           │
│ └──────────────────────┘ │    ├────────────────────────────┤
│                          │    │ - command: [python, script]│
│ ┌─ Script File ────────┐ │    │ - capture_output: True     │
│ │ Path: [___][Browse]  │ │    │ - text: True               │
│ └──────────────────────┘ │    │ - timeout: 60              │
│                          │    │ - cwd: script_dir          │
│ [Test] [Cancel] [Save]   │    └────────────┬───────────────┘
└──────────┬───────────────┘                 │
           │                                 │
           │ Save settings                   │ Result
           │                                 │
           ▼                                 ▼
┌──────────────────────────┐    ┌────────────────────────────┐
│ Config System            │    │ ScriptOutputDialog         │
│ (~/.math_exam_creator/)  │    │ (Results Display)          │
├──────────────────────────┤    ├────────────────────────────┤
│ config.json:             │    │ Script: [Name]             │
│ {                        │    │ Exit Code: [0] (Success)   │
│   "external_scripts": {  │    │                            │
│     "script1": {         │    │ [標準出力][エラー][全て] │
│       "name": "...",     │    │ ┌────────────────────────┐│
│       "python_path": "", │    │ │                        ││
│       "script_path": ""  │    │ │ Script output...       ││
│     }                    │    │ │                        ││
│   }                      │    │ └────────────────────────┘│
│ }                        │    │                            │
└──────────────────────────┘    │           [Close]          │
                                └────────────────────────────┘
```

## Data Flow

### Configuration Flow

```
User Input
    │
    ├─> Script Name ────────┐
    ├─> Description ────────┤
    ├─> Python Path ────────├──> ExternalScriptsDialog
    └─> Script Path ────────┘         │
                                      │ Save
                                      ▼
                              Config System
                           (JSON Persistence)
                                      │
                                      │ Load
                                      ▼
                            Main Window (Startup)
                                      │
                                      │ update_external_scripts_menu()
                                      ▼
                              Tools Menu Items
                           (Dynamic Menu Population)
```

### Execution Flow

```
User Clicks Menu Item (▶ Script Name)
    │
    ▼
execute_external_script(script_data)
    │
    ├─> Validate Python Path ────┐
    ├─> Validate Script Path ────┤
    └─> Show Confirmation ───────┘
            │
            │ User confirms
            ▼
    subprocess.run([python, script])
            │
            ├─> Capture stdout
            ├─> Capture stderr
            └─> Get return code
            │
            ▼
    ScriptOutputDialog
            │
            ├─> Display stdout (Tab 1)
            ├─> Display stderr (Tab 2)
            └─> Display combined (Tab 3)
            │
            ▼
    User Reviews Results
```

## Component Interaction Diagram

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Main      │         │  External   │         │   Script    │
│   Window    │◄────────┤  Scripts    │────────►│   Output    │
│             │ Creates │   Dialog    │ Creates │   Dialog    │
└──────┬──────┘         └──────┬──────┘         └─────────────┘
       │                       │
       │ Uses                  │ Uses
       │                       │
       ▼                       ▼
┌─────────────┐         ┌─────────────┐
│   Config    │         │ Subprocess  │
│   System    │         │   Module    │
└─────────────┘         └─────────────┘
```

## Class Diagram

```
┌─────────────────────────────────────┐
│     MainWindow (QMainWindow)        │
├─────────────────────────────────────┤
│ - current_project: Project          │
│ - problem_editors: List[Editor]     │
├─────────────────────────────────────┤
│ + open_external_scripts_settings()  │
│ + update_external_scripts_menu()    │
│ + execute_external_script(dict)     │
└──────────┬──────────────────────────┘
           │
           │ creates
           ▼
┌─────────────────────────────────────┐
│   ExternalScriptsDialog (QDialog)   │
├─────────────────────────────────────┤
│ - script_configs: List[dict]        │
│ - tab_widget: QTabWidget            │
├─────────────────────────────────────┤
│ + create_script_tab(int): dict      │
│ + browse_python(QLineEdit)          │
│ + browse_script(QLineEdit)          │
│ + test_current_script()             │
│ + execute_script(str,str,str)       │
│ + load_settings()                   │
│ + save_and_close()                  │
│ + get_all_scripts(): list           │
└──────────┬──────────────────────────┘
           │
           │ creates
           ▼
┌─────────────────────────────────────┐
│   ScriptOutputDialog (QDialog)      │
├─────────────────────────────────────┤
│ - script_name: str                  │
│ - stdout: str                       │
│ - stderr: str                       │
│ - return_code: int                  │
├─────────────────────────────────────┤
│ + create_output_tab(str,bool): QWidget │
└─────────────────────────────────────┘
```

## State Machine

```
┌──────────┐
│   Idle   │ Initial State
└────┬─────┘
     │
     │ User opens External Scripts Settings
     ▼
┌──────────────┐
│ Configuring  │ User edits script settings
└─────┬────────┘
      │
      │ User clicks Save
      ▼
┌─────────────┐
│   Saved     │ Settings persisted to config
└─────┬───────┘
      │
      │ Menu updated
      ▼
┌─────────────┐
│   Ready     │ Scripts available in menu
└─────┬───────┘
      │
      │ User clicks script menu item
      ▼
┌─────────────┐
│ Confirming  │ Show confirmation dialog
└─────┬───────┘
      │
      │ User confirms
      ▼
┌─────────────┐
│  Executing  │ Script running (60s timeout)
└─────┬───────┘
      │
      │ Execution completes
      ▼
┌─────────────┐
│  Showing    │ Display results dialog
│  Results    │
└─────┬───────┘
      │
      │ User closes dialog
      ▼
┌─────────────┐
│   Ready     │ Back to ready state
└─────────────┘
```

## File Structure

```
src/
├── main_window.py                     # Main application window
├── config.py                          # Configuration management
├── dialogs/
│   ├── __init__.py                    # Dialog exports
│   ├── external_scripts_dialog.py     # Configuration dialog
│   └── script_output_dialog.py        # Output display dialog
│
test_scripts/                          # Example scripts
├── test_script_1.py                   # Basic test
├── test_script_2.py                   # LaTeX formulas
└── test_script_3_error.py             # Error handling
│
tests/
└── test_external_scripts.py           # Unit tests
│
docs/
└── external_scripts_architecture.md   # This file
```

## Configuration Schema

```json
{
  "external_scripts": {
    "script1": {
      "name": "string",              // Display name in menu
      "description": "string",        // Optional tooltip
      "python_path": "string",        // Path to Python interpreter
      "script_path": "string"         // Path to .py file
    },
    "script2": { /* same schema */ },
    "script3": { /* same schema */ }
  }
}
```

## Error Handling

```
┌─────────────────┐
│ Execute Script  │
└────────┬────────┘
         │
         ├─> Script file not found ──> Show warning dialog
         │
         ├─> Python not found ──────> Show warning dialog
         │
         ├─> Timeout (60s) ─────────> Show timeout dialog
         │
         └─> Other exception ───────> Show error dialog
```

## Security Considerations

1. **Path Validation**: All file paths are validated before execution
2. **Confirmation Dialog**: User must confirm before script execution
3. **Timeout**: 60-second timeout prevents infinite loops
4. **Working Directory**: Scripts run in their own directory
5. **No Shell Injection**: Uses subprocess.run() without shell=True
6. **Error Isolation**: Exceptions caught and displayed safely

## Performance Considerations

1. **Asynchronous Execution**: Scripts run in subprocess (non-blocking)
2. **Timeout Limit**: 60-second maximum execution time
3. **Output Capture**: Buffered stdout/stderr capture
4. **Config Caching**: Settings loaded once at startup
5. **Menu Update**: Dynamic menu updates only when settings change

## Testing Strategy

```
Unit Tests
├── File existence tests
├── Script execution tests
│   ├── Success case
│   ├── Error case
│   └── Output validation
└── Module import tests

Integration Tests
└── End-to-end workflow test
    ├── Open dialog
    ├── Configure script
    ├── Save settings
    ├── Execute script
    └── Verify results

Manual Tests
├── UI interaction testing
├── Cross-platform testing
└── Edge case testing
```

## Cross-Platform Compatibility

| Feature             | Windows | macOS | Linux |
|---------------------|---------|-------|-------|
| Dialog UI           | ✅      | ✅    | ✅    |
| File browsing       | ✅      | ✅    | ✅    |
| Python detection    | ✅      | ✅    | ✅    |
| Script execution    | ✅      | ✅    | ✅    |
| Output capture      | ✅      | ✅    | ✅    |
| Config persistence  | ✅      | ✅    | ✅    |

## Future Enhancement Ideas

1. **Script Parameters**: Add support for command-line arguments
2. **Environment Variables**: Configure environment for script execution
3. **Output Formatting**: Syntax highlighting for different output types
4. **Script Templates**: Provide common script templates
5. **Script Library**: Share scripts between users
6. **Execution History**: Track script execution history
7. **Scheduled Execution**: Run scripts at specific times
8. **Script Validation**: Pre-execution validation/linting
