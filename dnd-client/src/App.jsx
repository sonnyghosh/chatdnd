import { useState } from 'react'
import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import {Navbar, StoryContainer} from './components'; 
// import './App.css'

function App() {


  return (
    <div className='bg-black'>
      <Navbar />
      <StoryContainer />  
    </div>
  )
}

export default App
