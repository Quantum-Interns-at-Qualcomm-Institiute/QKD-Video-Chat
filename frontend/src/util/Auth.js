async function isValidCode(code) {

    let isDigit = /^\d+$/.test(code);
    if (isDigit && code != "" && code.length == 8) return {ok: true}
    return {ok: false};
}

export {isValidCode};