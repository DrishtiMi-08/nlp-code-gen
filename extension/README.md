# Code Generator Extension

A VS Code extension that generates code on-the-fly using a magic comment `@gen`.

## Features

- **Type `@gen <prompt>` and press Enter** to generate code
- Shows loading indicator in status bar
- Replaces the `@gen` line with generated code
- Supports any programming language

## How to Use

1. In any file, type: `@gen describe what code you want`
2. Press **Enter** to trigger code generation
3. Watch the status bar for "Generating code..." message
4. The `@gen` line is automatically replaced with the generated code

### Example

**Before:**
```
@gen function to calculate fibonacci numbers
```

**After (once API responds):**
```
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Installation & Setup

### Prerequisites
- Node.js and npm installed
- VS Code 1.60 or later

### Build the Extension

```bash
cd /Users/soniasohal/Desktop/nlp-code-gen/extension

# Install dependencies
npm install

# Compile TypeScript to JavaScript
npm run compile
```

### Run in Development Mode

```bash
# Open the extension folder in VS Code
code .

# Press F5 to launch the extension in a new VS Code window
```

### Package for Distribution

```bash
# Install vsce (VS Code Extension packaging tool)
npm install -g vsce

# Package the extension
vsce package
```

This creates a `.vsix` file that can be installed in VS Code.

## API Configuration

The extension connects to: `http://127.0.0.1:8067/generate`

Make sure the backend server is running before using the extension:

```bash
cd /Users/soniasohal/Desktop/nlp-code-gen/backend
uvicorn main:app --reload --port 8067
```

## Development

### File Structure

```
extension/
├── src/
│   └── extension.ts       # Main extension logic
├── dist/
│   └── extension.js       # Compiled JavaScript
├── package.json           # Extension manifest
├── tsconfig.json         # TypeScript configuration
├── .vscodeignore         # Files to ignore in package
└── README.md            # This file
```

### Editing

1. Edit `src/extension.ts`
2. Run `npm run compile` to build
3. Reload the extension window (Ctrl+R or Cmd+R)

## Troubleshooting

- **"Failed to generate code: connect ECONNREFUSED"** → Backend server not running
- **Status bar shows error** → Check if API endpoint is correct
- **Extension not activating** → Reload VS Code window

## License

MIT
