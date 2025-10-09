import { useState } from 'react';

const SimpleTest = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const testBackend = async () => {
    console.log('🚀 [TEST] Starting simple backend test...');
    setLoading(true);
    
    try {
      console.log('🚀 [TEST] Making fetch request...');
      const res = await fetch('https://api.orchestratex.me/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message || 'test message' }),
      });

      console.log('🚀 [TEST] Response received:', res.status);
      
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();
      console.log('🚀 [TEST] Data:', data);
      setResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('❌ [TEST] Error:', error);
      setResponse(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', backgroundColor: '#1e293b', color: 'white', minHeight: '100vh' }}>
      <h1>🔧 Backend Connection Test</h1>
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Test message"
          style={{ padding: '10px', marginRight: '10px', width: '300px' }}
        />
        <button onClick={testBackend} disabled={loading} style={{ padding: '10px 20px' }}>
          {loading ? 'Testing...' : 'Test Backend'}
        </button>
      </div>
      <div style={{ backgroundColor: '#374151', padding: '20px', borderRadius: '8px' }}>
        <h3>Response:</h3>
        <pre style={{ whiteSpace: 'pre-wrap', fontSize: '12px' }}>
          {response || 'No response yet...'}
        </pre>
      </div>
    </div>
  );
};

export default SimpleTest;