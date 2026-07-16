async function register() {

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const response = await fetch(
        "http://127.0.0.1:5000/api/register",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    const result = await response.json();

    alert(result.message);

    if(result.message === "Registration Successful"){
        window.location.href = "/";
    }
}


async function login() {

    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const response = await fetch(
        "http://127.0.0.1:5000/api/login",
        {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    const result = await response.json();

    alert(result.message);

    if(result.message === "Login Successful"){
        window.location.href = "/dashboard";
    }
}