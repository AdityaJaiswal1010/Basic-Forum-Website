src = "https://smtpjs.com/v3/smtp.js";

const container = document.querySelector(".container"),
    pwShowHide = document.querySelectorAll(".showHidePw"),
    pwFields = document.querySelectorAll(".password"),
    signUp = document.querySelector(".signup-link"),
    login = document.querySelector(".login-link");

//   js code to show/hide password and change icon
pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        pwFields.forEach(pwField => {
            if (pwField.type === "password") {
                pwField.type = "text";

                pwShowHide.forEach(icon => {
                    icon.classList.replace("uil-eye-slash", "uil-eye");
                })
            } else {
                pwField.type = "password";

                pwShowHide.forEach(icon => {
                    icon.classList.replace("uil-eye", "uil-eye-slash");
                })
            }
        })
    })
})

// js code to appear signup and login form
signUp.addEventListener("click", () => {
    container.classList.add("active");
});

login.addEventListener("click", () => {
    container.classList.remove("active");
});

console.log(email)

let mainc;

function generateRandomNumber(numberOfCharacters) {
    var randomValues = '';
    var stringValues = 'ABCDEFGHIJKLMNOabcdefghijklmnopqrstuvwxyzPQRSTUVWXYZ123456789';
    var sizeOfCharacter = stringValues.length;
    for (var i = 0; i < numberOfCharacters; i++) {
        randomValues = randomValues + stringValues.charAt(Math.floor(Math.random() * sizeOfCharacter));
    }
    return randomValues;
}

function getemail() {
    let email = document.getElementById("email").value;
    //document.write(email);
    //let elength = email.length;
    let suffix = '@sakec.ac.in';
    let result = email.endsWith(suffix);
    if (result) {
        let maincode = generateRandomNumber(6);

        localStorage.setItem('otp', maincode);
        let vcode = maincode;
        //  console.log(vcode);
        //  console.log(maincode);
        //document.write("Congratulations Valid email");

        sendemail(email, vcode);
    } else {
        alert("Enter You sakec mail id !");
    }

}


function sendemail(email, vcode) {
    //var name = document.getElementById("name").value;

    Email.send({
        Host: "smtp.elasticemail.com",
        Username: "adityajaiswal9820@gmail.com",
        Password: "35A30E5639B1B24E665025CC4D9F4B19D24C",
        To: email,
        From: "adityajaiswal9820@gmail.com",
        Subject: "This is the verification code ",
        Body: vcode,
    }).then(
        message => {
            if (message == 'OK') {
                //checkverify(vcode);
                alert("The verification mail has been send ");
            } else {
                console.error(message);
                alert("Error occured");
            }
        }
    );
}

function checkverify() {
    var verify = document.getElementById("verification").value;


    var mainc = localStorage.getItem('otp');


    if (mainc === verify) {
        alert("Correct Verification code");
        localStorage.clear();
        // const flag = "1";
        // const dict_flag = { flag };
        // const s = JSON.stringify(dict_flag);
        // $.ajax({
        //     url: '/signup',
        //     type: "POST",
        //     contentType: "application/json",
        //     data: JSON.stringify(s)
        // });
        localStorage.setItem('flag', '1');

    } else {
        alert("Wrong Verification");
    }

}

function val() {
    var verify = document.getElementById("verification").value;
    return verify;
}