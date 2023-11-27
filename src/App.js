import React, {useState, useEffect} from "react";
import { BrowserRouter, Link, Routes, Route} from "react-router-dom";
import { Navbar } from "./components";

function App() {
    return (
        <div className = "App">
           <Navbar /> 
        </div>
    );
}

export default App;