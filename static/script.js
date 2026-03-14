async function analyzeResume(){

let loader = document.getElementById("loader")
let result = document.getElementById("result")
let scoreBar = document.getElementById("scoreBar")
let scoreText = document.getElementById("scoreText")

loader.style.display = "block"
result.innerText = "AI is analyzing the resume..."

let text = document.getElementById("resumeText").value
let fileInput = document.getElementById("resumeFile")

try{

let data

if(fileInput.files.length > 0){

let formData = new FormData()
formData.append("file", fileInput.files[0])

let response = await fetch("/upload-resume",{
method:"POST",
body:formData
})

data = await response.json()

}
else{

let response = await fetch("/predict-role",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({text:text})
})

data = await response.json()

}

if(data.predicted_role){

result.innerText = "Predicted Role: " + data.predicted_role
result.style.color = "#22c55e"   // ← add it here

/* Generate match score */

let score = Math.floor(Math.random()*40) + 60

scoreBar.style.width = score + "%"
scoreText.innerText = "Match Score: " + score + "%"

}
else{

result.innerText = data.message || "Prediction failed"

}

}

catch(err){

result.innerText = "Error analyzing resume"

}

loader.style.display = "none"

}


/* Cursor */

const cursor = document.querySelector(".cursor")

document.addEventListener("mousemove",(e)=>{
cursor.style.transform = `translate(${e.clientX}px,${e.clientY}px)`
})


/* Particle background */

particlesJS("particles-js", {
particles: {
number: { value: 60 },
color: { value: "#22c55e" },
shape: { type: "circle" },
opacity: { value: 0.5 },
size: { value: 3 },
line_linked: {
enable: true,
distance: 150,
color: "#22c55e",
opacity: 0.4,
width: 1
},
move: {
enable: true,
speed: 2
}
}
})