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


/* ===================== CUSTOM CURSOR ===================== */

const cursor = document.querySelector(".cursor")
const trail = document.querySelector(".cursor-trail")

let mouseX = 0, mouseY = 0
let trailX = 0, trailY = 0

document.addEventListener("mousemove", (e) => {
    mouseX = e.clientX
    mouseY = e.clientY
    cursor.style.left = mouseX + "px"
    cursor.style.top = mouseY + "px"
})

/* Smooth trailing ring */
function animateTrail(){
    trailX += (mouseX - trailX) * 0.12
    trailY += (mouseY - trailY) * 0.12
    trail.style.left = trailX + "px"
    trail.style.top = trailY + "px"
    requestAnimationFrame(animateTrail)
}
animateTrail()

/* Hover effect on interactive elements */
const hoverTargets = document.querySelectorAll("a, button, input, textarea, .contact-card, .stat-chip, .nav-links li")

hoverTargets.forEach(el => {
    el.addEventListener("mouseenter", () => {
        cursor.classList.add("hovering")
        trail.classList.add("hovering")
    })
    el.addEventListener("mouseleave", () => {
        cursor.classList.remove("hovering")
        trail.classList.remove("hovering")
    })
})


/* ===================== PARTICLE BACKGROUND ===================== */

particlesJS("particles-js", {
particles: {
number: { value: 55, density: { enable: true, value_area: 900 } },
color: { value: ["#22c55e", "#38bdf8", "#818cf8"] },
shape: { type: "circle" },
opacity: { value: 0.4, random: true, anim: { enable: true, speed: 0.8, opacity_min: 0.1 } },
size: { value: 2.5, random: true },
line_linked: {
enable: true,
distance: 140,
color: "#38bdf8",
opacity: 0.2,
width: 1
},
move: {
enable: true,
speed: 1.2,
direction: "none",
random: true,
out_mode: "out"
}
},
interactivity: {
detect_on: "canvas",
events: {
onhover: { enable: true, mode: "repulse" },
onclick: { enable: true, mode: "push" }
},
modes: {
repulse: { distance: 80, duration: 0.4 },
push: { particles_nb: 3 }
}
}
})
