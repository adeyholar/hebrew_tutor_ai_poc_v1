import { useState } from 'react';

function App() {
  const [message, setMessage] = useState('HebRabbAI Loading...');

  return (
    <div className="p-4 text-center">
      <h1 className="text-3xl font-bold">HebRabbAI Test UI</h1>
      <p>{message}</p>
      <button onClick={() => setMessage('Verified!')} className="bg-blue-500 text-white p-2 mt-2">Test State</button>
    </div>
  );
}

export default App;