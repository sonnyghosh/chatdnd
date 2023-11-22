import React, {useState, useEffect} from "react";
import { BrowserRouter, Link, Routes, Route} from "react-router-dom";
import './App.css';

function App() {
    const [currentTime, setCurrentTime] = useState(0);

    useEffect(() => {
        fetch('/api/time').then(res => res.json()).then(data => {
            setCurrentTime(data.time);
        });
    }, []);

    return (
        <div className = "App">
            <header className = "App-header">
                <BrowserRouter>
                    <div>
                        <Link className="App-link" to="/">Home</Link>
                        &nbsp;|&nbsp;
                        <Link className="App-link" to="/page2">Page2</Link>
                    </div>
                </BrowserRouter>
                <Routes>
                    <Route exact path ="/">
                        <p>
                            Edit <code>src/App.js</code> and save to reload.
                        </p>
                        <a 
                        className="App-link"
                        href="https://reactjs.org"
                        target="_blank"
                        rel="noopener noreferrer"
                        >
                            Learn React
                        </a>
                        <p>The current time is {currentTime}.</p>
                    </Route>
                    <Route path="/page2">
                        This is page 2!
                    </Route>
                </Routes>
            </header>
        </div>
    );
}

export default App;