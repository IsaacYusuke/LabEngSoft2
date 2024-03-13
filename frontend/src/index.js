import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./pages/Layout/Layout";
import Layout2 from "./pages/Layout2/Layout2";
import App from './App';

import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>

          <Route index element={<Layout />} />
          <Route path="teste" element={<Layout2 />} />
          
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
