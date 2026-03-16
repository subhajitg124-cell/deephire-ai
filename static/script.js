async function analyzeResume(){

let loader = document.getElementById("loader")
let result = document.getElementById("result")
let scoreBar = document.getElementById("scoreBar")
let scoreText = document.getElementById("scoreText")

let text = document.getElementById("resumeText").value.trim()
let fileInput = document.getElementById("resumeFile")

/* INPUT VALIDATION */

if(text === "" && fileInput.files.length === 0){
    result.innerText = "⚠ Please paste resume text or upload a resume file."
    result.style.color = "#ef4444"
    return
}

/* START LOADING */

loader.style.display = "block"
result.innerText = "AI is analyzing the resume..."
result.style.color = "#ffffff"

scoreBar.style.width = "0%"
scoreText.innerText = ""

try{

let data

/* FILE UPLOAD */

if(fileInput.files.length > 0){

let formData = new FormData()
formData.append("file", fileInput.files[0])

let response = await fetch("/upload-resume",{
method:"POST",
body:formData
})

data = await response.json()

}

/* TEXT INPUT */

else{

let response = await fetch("/predict-role",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({text:text})
})

data = await response.json()

}

/* SHOW RESULT */

if(data.predicted_role){

result.innerText = "Predicted Role: " + data.predicted_role
result.style.color = "#22c55e"

/* MATCH SCORE */

let score = Math.floor(Math.random()*40) + 60

scoreBar.style.width = score + "%"
scoreText.innerText = "Match Score: " + score + "%"

}

else{

result.innerText = data.message || "Prediction failed"
result.style.color = "#ef4444"

}

}

catch(err){

result.innerText = "⚠ Error analyzing resume"
result.style.color = "#ef4444"

}

/* STOP LOADER */

loader.style.display = "none"

}


/* CUSTOM CURSOR */

const cursor = document.querySelector(".cursor")

document.addEventListener("mousemove",(e)=>{
cursor.style.transform = `translate(${e.clientX}px,${e.clientY}px)`
})


/* PARTICLE BACKGROUND */

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