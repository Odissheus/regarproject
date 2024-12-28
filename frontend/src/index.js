import React from "react";
import ReactDOM from "react-dom";
import "./index.css"; // Assicurati che esista se è importato

const App = () => {
    return (
        <div>
            <h1>Hello, React!</h1>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById("root"));
