import React, {useState, useEffect} from "react";
import { BrowserRouter, Link, Routes, Route} from "react-router-dom";
import './App.css';

function App() {
    console.log("start of app");
    const [currentTime, setCurrentTime] = useState(0);

    console.log("before api call");

    useEffect(() => {
        fetch('api/time').then(res => res.json()).then(data => {
            setCurrentTime(data.time);
        }).catch(
            error => {
                console.error('Error fetching data:', error);
            }
        );
    }, []);

    console.log("after api calling");

    return (
        <div className = "App">
            <header className = "App-header">
                <BrowserRouter>
                    <div>
                        <Link className="App-link" to="/">Home</Link>
                        &nbsp;|&nbsp;
                        <Link className="App-link" to="/page2">Page2</Link>
                    </div>
                
                    <Routes>
                        <Route exact path ="/" element ={
                            <React.Fragment>
                            <p>
                                Edit <code>src/App.js</code> and save to reload.
                            </p>
                            <a 
                                className="App-link"
                                href="https://reactjs.org"
                                target="_blank"
                                rel="noopener noreferrer">
                                Learn React
                            </a>
                            <p>The current time is {currentTime}.</p>
                        </React.Fragment>
                    }/>
                        <Route path="/page2" element = {<div>This is page 2!</div>}/>
                    </Routes>
               </BrowserRouter> 
            </header>
        </div>
    );
}

export default App;