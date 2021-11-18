document.getElementById('signbtn').addEventListener('click', mohit)


async function mohit() {
    document.getElementById("signbtn").disabled = true;
    document.getElementById("spinner").style.display = "inline-block";
    let response = await fetch('/register/setcache', {
        credentials: 'include',
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "email": document.getElementById("email").value,
            "password": document.getElementById("password").value,
            "first_name": document.getElementById("first_name").value,
            "last_name": document.getElementById("last_name").value,
            "cpassword": document.getElementById("cpassword").value,
            "username": document.getElementById("email").value
        })
    })
    if (response.ok) {
        document.getElementById("signbtn").disabled = false;
        document.getElementById('spinner').style.display = 'none';
        // document.getElementById("verifier").style.display = 'block';
        let json = await response.json();
        let message = json["message"]
        alert(message);
        if (message == 'otp send.' || message == "Otp Already send please wait for 5 minutes for resend.") {
            document.getElementById("otp").style.display = "block";
            try {
                document.getElementById('signbtn').removeEventListener('click', mohit);
            } catch (err) {}
            document.getElementById('signbtn').id = "signbtnsbmit";
            document.getElementById('signbtnsbmit').addEventListener('click', async function() {
                document.getElementById("signbtnsbmit").disabled = true;
                document.getElementById("spinner").style.display = "inline-block";
                let response = await fetch('/register/verify', {
                    credentials: 'include',
                    method: 'POST',
                    mode: 'same-origin',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "email": document.getElementById("email").value,
                        "otp": document.getElementById("otp").value
                    })
                })
                if (response.ok) {
                    document.getElementById('spinner').style.display = 'none';
                    document.getElementById("signbtnsbmit").disabled = false;
                    // document.getElementById("verifier").style.display = 'block';
                    let json = await response.json();
                    let message = json["message"]
                    alert(message);
                    if (message == 'success') {
                        window.location.replace('/')
                    }

                } else {
                    document.getElementById("spinner").style.display = "none";
                    document.getElementById("signbtnsbmit").disabled = false;
                    alert("HTTP-Error: " + response.status);
                }
            })
        }

    } else {
        document.getElementById("spinner").style.display = "none";
        document.getElementById("signbtn").disabled = false;
        alert("HTTP-Error: " + response.status);

    }
}