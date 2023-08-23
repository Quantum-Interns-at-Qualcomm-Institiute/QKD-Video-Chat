import {useState} from "react";
import {useNavigate} from "react-router-dom";
import Header from "../components/Header";
import {isValidCode} from "../util/Auth";
import { Snackbar } from "@material-ui/core";

import "../css/Start.css"

export default function Start() {
    const navigate = useNavigate();
    const [code, setCode] = useState("");
    const [error, setError] = useState({
        open: false,
        message: "An error has occured.",
    });

    function handleCodeChange(e) {
        setCode(e.target.value);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await isValidCode(code);
        if(response.ok) navigate("/session")
        // else show error
    }

    return (
        <>
            <Header />
            <div class="start-content">
                <form class="codeForm" onSubmit={handleSubmit}>
                    <input type="text" placeholder="Code" name="code" id="code" onChange={handleCodeChange}/>
                    <button type="submit">Connect</button>
                </form>
            </div>

            <Snackbar
                open={error.open}
                autoHideDuration={6000}
                onClose={(e,reason) => {
                    if(reason === "clickaway") return;
                    setError({...state})
                }}
            />
        </>
    )
}