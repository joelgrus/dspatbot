# --- BEGIN RECONSTRUCTED FILE ---
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from .chatbot import Chatbot
from .history.basic import BasicHistoryManager
from .llm import configure_llm

configure_llm()

HTML_PAGE = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Chatbot</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #f7f7fa; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
    h1 { margin-top: 2em; color: #333; letter-spacing: 1px; }
    #chat-container { background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); padding: 2em 2em 1em 2em; margin: 2em 0; width: 100%; max-width: 420px; min-width: 280px; }
    #new-convo { margin-bottom: 1em; background: #e0e7ff; border: none; border-radius: 4px; padding: 0.5em 1.2em; font-size: 1em; cursor: pointer; transition: background 0.2s; }
    #new-convo:hover { background: #c7d2fe; }
    #chat-form { display: flex; gap: 0.5em; margin-bottom: 1em; }
    #message { flex: 1; padding: 0.5em; border: 1px solid #bbb; border-radius: 4px; font-size: 1em; }
    #chat-form button[type=submit] { background: #6366f1; color: #fff; border: none; border-radius: 4px; padding: 0.5em 1.2em; font-size: 1em; cursor: pointer; transition: background 0.2s; }
    #chat-form button[type=submit]:hover { background: #4f46e5; }
    #chat-history { white-space: pre-wrap; border: 1px solid #ccc; border-radius: 4px; background: #f3f4f6; padding: 1em; min-height: 8em; margin-bottom: 1em; font-size: 1em; max-height: 300px; overflow-y: auto; }
    #chat-history div { margin-bottom: 0.5em; }
    #chat-history b { color: #6366f1; font-weight: 600; margin-right: 0.5em; }
  </style>
</head>
<body>
  <h1>Chatbot</h1>
  <div id='chat-container'>
    <button id='new-convo' type='button'>New Conversation</button>
    <form id='chat-form'>
      <input type='text' id='message' name='message' autocomplete='off' placeholder='Type your message...' required>
      <button type='submit'>Send</button>
    </form>
    <div id='chat-history'></div>
  </div>
  <script>
    let conversationId = 0;
    const form = document.getElementById('chat-form');
    const input = document.getElementById('message');
    const button = form.querySelector('button[type="submit"]');
    const historyDiv = document.getElementById('chat-history');
    const newConvoBtn = document.getElementById('new-convo');
    function appendMessage(role, text) {
      const label = role === 'user' ? 'user:' : 'assistant:';
      const msgDiv = document.createElement('div');
      msgDiv.innerHTML = `<b>${label}</b> ${text}`;
      historyDiv.appendChild(msgDiv);
      historyDiv.scrollTop = historyDiv.scrollHeight;
    }
    form.onsubmit = async function(e) {
      e.preventDefault();
      input.disabled = true;
      button.disabled = true;
      const msg = input.value;
      appendMessage('user', msg);
      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({message: msg, conversation_id: conversationId})
        });
        const data = await res.json();
        appendMessage('assistant', data.answer || data.error);
        input.value = '';
      } finally {
        input.disabled = false;
        button.disabled = false;
        input.focus();
      }
    };
    newConvoBtn.onclick = function() {
      conversationId++;
      historyDiv.innerHTML = '';
      input.value = '';
      input.focus();
    };
  </script>
</body>
</html>
"""

# --- END HTML_PAGE ---

history_manager = BasicHistoryManager()
chatbot = Chatbot(history_manager)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                message = data.get('message', '')
                conversation_id = str(data.get('conversation_id', '0'))
                result = chatbot.forward(query=message, session_id=conversation_id)
                answer = getattr(result, 'answer', None)
                response = {'answer': answer}
            except Exception as e:
                response = {'error': str(e)}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
