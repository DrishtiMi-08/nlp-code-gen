import * as vscode from 'vscode';
import axios from 'axios';

const API_URL = 'https://railway.com/project/febceb98-9ab4-41ae-87dc-b9c2211d8cb9';

export function activate(context: vscode.ExtensionContext) {
  const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);

  // Listen for text edits
  const disposable = vscode.workspace.onDidChangeTextDocument(async (event) => {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document !== event.document) {
      return;
    }

    // Check each change for Enter key (indicated by newline in contentChanges)
    for (const change of event.contentChanges) {
      // Detect when user presses Enter (text contains newline)
      if (change.text === '\n' || change.text.includes('\n')) {
        // Get the line before the newline was added
        const line = change.range.start.line;
        const lineText = editor.document.lineAt(line).text.trim();

        // Check if line contains @gen
        const genMatch = lineText.match(/^@gen\s+(.+)$/);
        if (genMatch && genMatch[1]) {
          const prompt = genMatch[1].trim();

          // Move cursor to the line and generate code
          setTimeout(async () => {
            await generateCode(editor, line, prompt, statusBar);
          }, 50);
        }
      }
    }
  });

  context.subscriptions.push(disposable, statusBar);
}

async function generateCode(
  editor: vscode.TextEditor,
  lineNumber: number,
  prompt: string,
  statusBar: vscode.StatusBarItem
) {
  try {
    // Show loading message
    statusBar.text = '$(loading~spin) Generating code...';
    statusBar.show();

    const response = await axios.post(API_URL, {
      raw_input: prompt,
    });

    if (response.data && response.data.code) {
      const generatedCode = response.data.code;

      // Replace the @gen line with generated code
      const line = editor.document.lineAt(lineNumber);
      const range = line.range;

      await editor.edit((editBuilder) => {
        editBuilder.replace(range, generatedCode);
      });

      // Show success message
      statusBar.text = '$(check) Code generated!';
      setTimeout(() => statusBar.hide(), 3000);

      vscode.window.showInformationMessage('✓ Code generated successfully!');
    } else {
      vscode.window.showErrorMessage('No code returned from API');
      statusBar.hide();
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    vscode.window.showErrorMessage(`Failed to generate code: ${errorMessage}`);
    statusBar.hide();
  }
}

export function deactivate() {}
