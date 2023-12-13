var card = document.getElementById("card");

function openRegister() {
	card.style.transform = "rotateY(-180deg)";
}

function openLogin(){
	card.style.transform = "rotateY(0deg)";
}

function saveData() {
        let name, email, password;
        name = document.getElementById("name").value;
        email = document.getElementById("email").value;
        password = document.getElementById("password").value;

        let user_records=new Array();
        user_records=JSON.parse(localStorage.getItem("users"))?JSON.parse(localStorage.getItem("users")):[]
        if(user_records.some((v)=>{
                return v.email==email
        })){
                alert("Duplicate Data");
        }
        else {
                user_records.push({
                        "name": name,
                        "email": email,
                        "password": password
                })
                localStorage.setItem("users", JSON.stringify(user_records));
}

function retrieveData() {
        let email, password;
        email = document.getElementById("email").value;
        password = document.getElementById("password").value;

        let user_record = new Array();
	user_records=JSON.parse(localStorage.getItem("users"))?JSON.parse(localStorage.getItem("users")):[]
        if(user_record.some((v)=> {
                return v.email===email && v.password===password
        })){
                alert("Login Successful")
                let current_user = user_record.filter((v)=> {
                        return v.email===email && v.password===password
                })[0]

                localStorage.setItem("name", current_user.name);
                localStorage.setItem("email", current_user.email);
                window.location.href="dashboard.html";
        }
        else {
                alert("Login Fail");
        }
}

// Function to handle logout
function logout() {
  fetch('/logout', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  }).then(response => response.json())
    .then(data => {
      if (data.message === 'Logout successful') {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      } else {
        alert(data.error);
      }
    })
    .catch(error => {
      console.error(error);
      alert('Internal server error. Please try again later.');
    });
}

// Add click event listener to logout button
// const logoutButton = document.getElementById('logout-button');
// logoutButton.addEventListener('click', logout);
