import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

THEMES = {
    "PurpleLight": {
        "primary": "#6200ea",
        "secondary": "#03dac6",
        "background": "#f5f5f5",
        "surface": "#ffffff",
        "error": "#b00020",
        "text": "#000000"
    },
    "BlueLight": {
        "primary": "#3b82f6",
        "secondary": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e42",
        "gray": "#6b7280",
        "background": "#f8fafc",
        "surface": "#ffffff",
        "text": "#000000"
    },
    "OceanLight": {
        "primary": "#0d6efd",
        "secondary": "#6c757d",
        "success": "#198754",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "background": "#f8f9fa",
        "surface": "#ffffff",
        "text": "#000000"
    },
    "DarkModern": {
        "background": "#181818",
        "surface": "#232323",
        "primary": "#1db954",
        "accent": "#bb86fc",
        "text": "#ffffff"
    }
}

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def create_folder(path: str):
    os.makedirs(path, exist_ok=True)
    return f"Folder created: {path}"

def create_file(path: str):
    with open(path, 'w') as f:
        f.write("")
    return f"File created: {path}"

def write_to_file(data: dict):
    path = data["path"]
    content = data["content"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    return f"Content written to {path}"

def read_file(path: str):
    with open(path, 'r') as f:
        return f.read()

def select_theme(_=None):
    themes = list(THEMES.keys())
    print("Select a theme for your React Todo app:")
    for i, theme in enumerate(themes, 1):
        print(f"{i}. {theme}")
    while True:
        choice = input("Enter number: ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(themes):
                selected = themes[idx]
                print(f"Theme selected: {selected}")
                return selected
        print("Invalid choice, try again.")

available_tools = {
    "select_theme": select_theme,
    "run_command": run_command,
    "create_folder": create_folder,
    "create_file": create_file,
    "write_to_file": write_to_file,
    "read_file": read_file
}

SYSTEM_PROMPT = """
    You are an helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tools. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    - Always ask the user to select a UI theme from predefined options as the first step for any project.
    - Always use .jsx files and the Vite react template unless the user requests TypeScript.
    - When writing to a file, always generate and include the full, working code for the component or file, not just a placeholder comment.
    - When generating component code including contents such as text, use the selected theme's colors or classes in the component styles, unless the user requests otherwise.
    - By default, always center the main component in the viewport using flexbox (justifyContent: 'center', alignItems: 'center', minHeight: '100vh', width: '100vw'), unless the user explicitly requests a different layout.
    - The assistant should support interactive sessions: after completing a task, always prompt the user for further instructions or changes (e.g., "Would you like to add, edit, or remove anything?").
    - If the user requests a change, update the project accordingly and show the result, then prompt again.

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.
    - "create_folder": Takes a folder path as an input and creates a folder at the given path.
    - "create_file": Takes a file path as an input and creates a file at the given path.
    - "write_to_file": Takes a file path and content as an input and writes the content to the file at the given path.
    - "read_file": Takes a file path as an input and returns the content of the file.
    - "select_theme" : Selects a theme from the predefined options.

    
    Example:
    User Query : Create a TODO app in React
    Output : {{"step" : "plan", "content" : "The user is interested in a TODO app using React"}}
    Output : {{"step" : "plan", "content" : "First ask the user to select a UI theme from predefined options"}}
    Output : {{"step" : "action", "function" : "select_theme", "input" : null }}
    Output : {{"step" : "observe", "output": "User selected the 'PurpleLight' theme with primary color #6200ea." }}
    Output : {{"step": "plan", "content": "Initialize a new React app folder using Vite with .jsx and .js"}}
    Output : {{"step": "action", "function": "run_command", "input": "npm create vite@latest todo-app -- --template react"}}
    Output : {{"step": "observe", "output": "React app created successfully in folder todo-app."}}
    Output : {{"step": "plan", "content": "Create components folder inside src directory."}}
    Output : {{"step": "action", "function": "create_folder", "input": "todo-app/src/components"}}
    Output : {{"step": "observe", "output": "components folder created."}}
    Output : {{"step": "plan", "content": "Write Todo.jsx React component file with select theme color inside components folder."}}
    Output : {{"step": "action", "function": "write_to_file", "input": {
    "path": "todo-app/src/components/Todo.jsx",
    "content": "import React, { useState } from 'react';\\n\\nconst Todo = () => {\\n  const [todos, setTodos] = useState([]);\\n  const [newTodo, setNewTodo] = useState('');\\n\\n  const addTodo = () => {\\n    if (newTodo.trim()) {\\n      setTodos([...todos, { id: Date.now(), text: newTodo.trim() }]);\\n      setNewTodo('');\\n    }\\n  };\\n\\n  const deleteTodo = (id) => {\\n    setTodos(todos.filter((todo) => todo.id !== id));\\n  };\\n\\n  return (\\n    <div style={{ background: '#f5f5f5', minHeight: '100vh', width: '100vw', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>\\n      <div style={{ background: '#fff', borderRadius: 12, boxShadow: '0 4px 24px rgba(0,0,0,0.08)', padding: 32, minWidth: 350, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>\\n        <h1 style={{ color: '#6200ea', fontWeight: 'bold', fontSize: 32, marginBottom: 24, textAlign: 'center' }}>Todo App</h1>\\n        <div style={{ display: 'flex', marginBottom: 24, width: '100%' }}>\\n          <input\\n            type='text'\\n            style={{ flex: 1, padding: 12, border: '1px solid #6200ea', borderRadius: 6, marginRight: 12, fontSize: 16 }}\\n            placeholder='Add a todo'\\n            value={newTodo}\\n            onChange={e => setNewTodo(e.target.value)}\\n          />\\n          <button\\n            style={{ background: '#6200ea', color: '#fff', fontWeight: 'bold', padding: '12px 24px', border: 'none', borderRadius: 6, fontSize: 16, cursor: 'pointer' }}\\n            onClick={addTodo}\\n          >\\n            Add\\n          </button>\\n        </div>\\n        <ul style={{ listStyle: 'none', padding: 0, margin: 0, width: '100%' }}>\\n          {todos.map((todo) => (\\n            <li key={todo.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid #f5f5f5' }}>\\n              <span style={{ fontSize: 16, color: '#000' }}>{todo.text}</span>\\n              <button\\n                style={{ background: '#b00020', color: '#fff', border: 'none', borderRadius: 4, padding: '6px 14px', fontSize: 14, cursor: 'pointer' }}\\n                onClick={() => deleteTodo(todo.id)}\\n              >\\n                Delete\\n              </button>\\n            </li>\\n          ))}\\n        </ul>\\n      </div>\\n    </div>\\n  );\\n};\\n\\nexport default Todo;\\n"
    }}}}}
    Output : {{"step": "observe", "output": "Todo.jsx file created with component code."}}
    Output : {{"step": "plan", "content": "Update App.jsx to import and render the Todo component."}}
    Output : {{"step": "action", "function": "write_to_file", "input": {{"path": "todo-app/src/App.jsx", "content": "import React from 'react';\\nimport Todo from './components/Todo';\\n\\nfunction App() {\\n  return (\\n    <div>\\n      <Todo />\\n    </div>\\n  );\\n}\\n\\nexport default App;\\n"}}}}
    Output : {{"step": "observe", "output": "App.jsx updated."}}
    Output : {{"step": "plan", "content": "Install node dependencies."}}
    Output : {{"step": "action", "function": "run_command", "input": "cd todo-app && npm install"}}
    Output : {{"step": "observe", "output": "Dependencies installed."}}
    # At this point, prompt the user for further changes:
    # (This is handled by your main loop, not the prompt itself.)
    # Only after the user says "no" or is done:
    Output : {{"step": "plan", "content": "Start the React development server."}}
    Output : {{"step": "action", "function": "run_command", "input": "cd todo-app && npm run dev"}}
    Output : {{"step": "observe", "output": "React app running at http://localhost:5173"}}
    Output : {{"step": "output", "content": "React Todo app has been created with the PurpleLight theme and is running at http://localhost:5173. You can now access it in your browser."}}
"""

messages = [
  { "role": "system", "content": SYSTEM_PROMPT }
]

while True:
    query = input("> ")
    messages.append({ "role": "user", "content": query })

    should_exit = False
    pending_final_steps = []

    while not should_exit:
        response = client.chat.completions.create(
            model="gemini-2.0-flash-lite",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({ "role": "assistant", "content": response.choices[0].message.content })
        print(response.choices[0].message.content)
        parsed_response = json.loads(response.choices[0].message.content)

        if isinstance(parsed_response, list):
            for step in parsed_response:
                if step.get("step") == "plan":
                    print(f"🧠: {step.get('content')}")
                elif step.get("step") == "action":
                    if step.get("function") == "run_command" and "npm run dev" in str(step.get("input")):
                        pending_final_steps.append(step)
                        continue
                    tool_name = step.get("function")
                    tool_input = step.get("input")
                    print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")
                    if available_tools.get(tool_name) is not False:
                        output = available_tools[tool_name](tool_input)
                        messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
                elif step.get("step") == "output":
                    pending_final_steps.append(step)
                    continue
            if pending_final_steps:
                next_action = input("✨ Would you like to make any changes or add something else before finishing? (Type your request or 'no' to finish): ")
                if next_action.strip().lower() in ["no", "exit", "quit"]:
                    for final_step in pending_final_steps:
                        if final_step.get("step") == "action":
                            tool_name = final_step.get("function")
                            tool_input = final_step.get("input")
                            print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")
                            if available_tools.get(tool_name) is not False:
                                output = available_tools[tool_name](tool_input)
                                messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
                        elif final_step.get("step") == "output":
                            print(f"🤖: {final_step.get('content')}")
                    pending_final_steps = []
                    should_exit = True
                    break
                else:
                    messages.append({ "role": "user", "content": next_action })
                    pending_final_steps = []
                    continue
        else:
            if parsed_response.get("step") == "plan":
                print(f"🧠: {parsed_response.get('content')}")
                continue
            if parsed_response.get("step") == "action":
                if parsed_response.get("function") == "run_command" and "npm run dev" in str(parsed_response.get("input")):
                    pending_final_steps.append(parsed_response)
                    continue
                tool_name = parsed_response.get("function")
                tool_input = parsed_response.get("input")
                print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")
                if available_tools.get(tool_name) is not False:
                    output = available_tools[tool_name](tool_input)
                    messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
                    continue
            if parsed_response.get("step") == "output":
                pending_final_steps.append(parsed_response)
                next_action = input("✨ Would you like to make any changes or add something else before finishing? (Type your request or 'no' to finish): ")
                if next_action.strip().lower() in ["no", "exit", "quit"]:
                    for final_step in pending_final_steps:
                        if final_step.get("step") == "action":
                            tool_name = final_step.get("function")
                            tool_input = final_step.get("input")
                            print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")
                            if available_tools.get(tool_name) is not False:
                                output = available_tools[tool_name](tool_input)
                                messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
                        elif final_step.get("step") == "output":
                            print(f"🤖: {final_step.get('content')}")
                    pending_final_steps = []
                    should_exit = True
                    break
                else:
                    messages.append({ "role": "user", "content": next_action })
                    pending_final_steps = []
                    continue