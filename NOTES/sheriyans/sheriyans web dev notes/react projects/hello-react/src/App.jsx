import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

import {FaBeer} from "react-icons/fa";


function App() {
  const name = "REact";
  return (
    <div>
      <h1>Hello, React! <FaBeer size={32} color="#61DAFB" /> </h1>
    </div>
  );
}

export default App
