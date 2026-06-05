import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const rootElementMountTarget = document.getElementById('root');
const virtualDomRootNode = ReactDOM.createRoot(rootElementMountTarget);

virtualDomRootNode.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
