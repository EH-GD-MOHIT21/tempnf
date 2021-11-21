document.getElementById('logbtn').addEventListener('click', mohit)


async function mohit() {
    document.getElementById("spinner").style.display = "inline-block";
    let response = await fetch('/login/setcache', {
        credentials: 'include',
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "username": document.getElementById("username").value,
            "password": document.getElementById("password").value
        })
    })
    if (response.ok) {
        document.getElementById('spinner').style.display = 'none';
        // document.getElementById("verifier").style.display = 'block';
        let json = await response.json();
        let message = json["message"]
        if (message == 'otp send.') {
            document.getElementById("otp").style.display = "block";
            document.getElementById("keyico").style.display = "block";
            try {
                document.getElementById('logbtn').removeEventListener('click', mohit);
            } catch (err) {}
            document.getElementById('logbtn').id = "logbtnsbmit";
            document.getElementById('logbtnsbmit').addEventListener('click', async function() {
                document.getElementById("spinner").style.display = "inline-block";
                let response = await fetch('/login/verify', {
                    credentials: 'include',
                    method: 'POST',
                    mode: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "username": document.getElementById("username").value,
                        "password": document.getElementById("password").value,
                        "otp": document.getElementById("otp").value
                    })
                })
                if (response.ok) {
                    document.getElementById('spinner').style.display = 'none';
                    // document.getElementById("verifier").style.display = 'block';
                    let json = await response.json();
                    let message = json["message"]
                    if (message == 'success') {
                        window.location.replace('/')
                    }

                } else {
                    document.getElementById('spinner').style.display = 'none';
                    alert("HTTP-Error: " + response.status);
                }
            })
        }

    } else {
        document.getElementById('spinner').style.display = 'none';
        alert("HTTP-Error: " + response.status);
    }
}