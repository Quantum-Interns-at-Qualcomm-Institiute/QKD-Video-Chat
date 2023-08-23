import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Start from "./screens/Start";

function App() {
    return (
        <Router>
            <Routes>
                {/* Home Page */}
                <Route path="/" element={<Start />}>
                </Route>

            </Routes>
        </Router>
    );
}

export default App;
