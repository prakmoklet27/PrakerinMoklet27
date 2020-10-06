const inputs = document.querySelectorAll(".form-control");


function addcl() {
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl() {
	let parent = this.parentNode.parentNode;
	if (this.value == "") {
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});

function yesnoCheck(that) {
	if (that.value == "perwakilan") {
		document.getElementById("ifYes").style.display = "block";
	} else {
		document.getElementById("ifYes").style.display = "none";
	}
}