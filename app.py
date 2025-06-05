import gradio as gr
from pathlib import Path
import traceback
from filesystem_access import FilesystemAccess
import os

fs = FilesystemAccess(os.getenv("FILES_DIR"))

allow_writes = os.getenv("ALLOW_EDITING") == "true" or os.getenv("ALLOW_EDITING") == "1"

def safe_exec(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        print(f"Not found: {str(e)}")
        return f"Error: Not found"
    except FileExistsError as e:
        print(f"Already exists: {str(e)}")
        return f"Error: Already exists"
    except Exception as e:
        print(f"Error: {str(e)}\n{traceback.format_exc()}")
        return f"Error"

def read_file(path):
    return safe_exec(fs.read_file, path)

def read_multiple_files(paths):
    path_list = [p.strip() for p in paths.split(',') if p.strip()]

    file_contents = []
    try: 
        for path in path_list:
            
            try:
                file_content = fs.read_file(path)
                file_contents.append(f"{path}:\n{file_content}\n")
            except Exception as e:
                file_contents.append(f"{path}:Error - Could not read file")
        return "\n---\n".join(file_contents)
    
    except Exception as e:
        print(f"Error: {str(e)}\n{traceback.format_exc()}")
        return f"Error"

def write_file(path, content):
    return safe_exec(fs.write_file, path, content) or "File written successfully."

def create_directory(path):
    return safe_exec(fs.create_directory, path) or "Directory ensured."

def list_directory(path):
    return '\n'.join(safe_exec(fs.list_directory, path))

def move_file(source, destination):
    return safe_exec(fs.move_file, source, destination) or "Move successful."

def search_files(path, pattern, exclude):
    exclude_list = [e.strip() for e in exclude.split(',') if e.strip()]
    return '\n'.join(safe_exec(fs.search_files, path, pattern, exclude_list))

def directory_tree(path):
    return safe_exec(fs.directory_tree, path)

with gr.Blocks() as demo:
    with gr.Tab("Read File"):
        path = gr.Textbox(label="Path", value="index.md")
        output = gr.Textbox(label="File Contents")
        btn = gr.Button("Read")
        btn.click(fn=read_file, inputs=path, outputs=output)

    with gr.Tab("Read Multiple Files"):
        paths = gr.Textbox(label="Comma-separated Paths", value="index.md,index.html")
        output = gr.Textbox(label="Results")
        btn = gr.Button("Read")
        btn.click(fn=read_multiple_files, inputs=paths, outputs=output)

    with gr.Tab("List Directory"):
        path = gr.Textbox(label="Directory Path", value=".")
        output = gr.Textbox(label="Contents")
        btn = gr.Button("List")
        btn.click(fn=list_directory, inputs=path, outputs=output)

    with gr.Tab("Directory Tree"):
        path = gr.Textbox(label="Directory Path", value=".")
        output = gr.Textbox(label="Contents")
        btn = gr.Button("Show Tree")
        btn.click(fn=directory_tree, inputs=path, outputs=output)

    with gr.Tab("Search Files"):
        path = gr.Textbox(label="Search Directory", value=".")
        pattern = gr.Textbox(label="Pattern", value="*.html")
        exclude = gr.Textbox(label="Exclude Patterns (comma-separated)", value="*.md")
        output = gr.Textbox(label="Matches")
        btn = gr.Button("Search")
        btn.click(fn=search_files, inputs=[path, pattern, exclude], outputs=output)

    if allow_writes:
        with gr.Tab("Write File"):
            path = gr.Textbox(label="Path", value="index.html")
            content = gr.Textbox(label="Content", lines=10, value="<html><body><h1>Hello World</h1></body></html>")
            output = gr.Textbox(label="Status")
            btn = gr.Button("Write")
            btn.click(fn=write_file, inputs=[path, content], outputs=output)

        with gr.Tab("Create Directory"):
            path = gr.Textbox(label="Directory Path", value="test")
            output = gr.Textbox(label="Status")
            btn = gr.Button("Create")
            btn.click(fn=create_directory, inputs=path, outputs=output)

        with gr.Tab("Move File"):
            source = gr.Textbox(label="Source Path", value="index.html")
            destination = gr.Textbox(label="Destination Path", value="test/index.html")
            output = gr.Textbox(label="Status")
            btn = gr.Button("Move")
            btn.click(fn=move_file, inputs=[source, destination], outputs=output)
    

if __name__ == "__main__":
    demo.launch()