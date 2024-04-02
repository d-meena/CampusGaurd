import React from 'react'
import {useNavigate} from 'react-router-dom'

function Home() {

    const navigate = useNavigate()

    return (
        <div>
          <h1>Home</h1>
          <button onClick={() => navigate('/entries')}>Go to Entries</button>
          <button onClick={() => navigate('/make_entry')}>Make a Entry</button>
        </div>
    );
    
}

export default Home