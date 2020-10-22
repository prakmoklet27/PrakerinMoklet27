const inputs = document.querySelectorAll(".form-control");
function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
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
		document.getElementById("penerima_kuasa").required = true;
		document.getElementById("myfile").required = true;
	} else {
		document.getElementById("ifYes").style.display = "none";
		document.getElementById("penerima_kuasa").required = false;
		document.getElementById("myfile").required = false;
	}
}

// const submit = document.querySelector('#submit');
// submit.addEventListener('click',function() {
// 	Swal.fire({
//   icon: 'success',
//   title: 'Registrasi Berhasil',
//   text: 'Terima kasih telah melakukan pendaftaran dan mengkonfirmasikan kehadiran Anda Password akun Anda telah dikirimkan melalui Email',
// });
// });

// $("#registrasiForm").submit(function(event) {
// 	console.log("Tes")
// 	event.preventDefault();
// 	var data    = $('#registrasiForm').serialize();                
// 	$.ajax({
// 		type: "POST",
// 		data: data,
// 		url: "/register/save",
// 		success: function(toni) {
// 		  if (toni.info.status == 0) {            
// 			swal(toni.info.intro,toni.info.pesan,toni.info.type)                    
// 		  }        
// 		  else {            
// 			swal(toni.info.intro,toni.info.pesan,toni.info.type)
// 			.then((beres) => {
// 			  window.location.assign("/"); 
// 			});                
// 		  }
// 		}
// 	});
//   });

$("#reset").submit(function(event) {
	console.log("Tes")
	event.preventDefault();
	var data = $('#reset').serialize();                
	$.ajax({
		type: "POST",
		data: data,
		url: "/reset_password",
		success: function(toni) {
			console.log(toni)
			if (toni.info.status == 0) {            
			Swal.fire(toni.info.intro,toni.info.pesan,toni.info.type)                    
		}  
		else {            
			Swal.fire(toni.info.intro,toni.info.pesan,toni.info.type)
			.then((beres) => {
			window.location.assign("/login"); 
			});              
		}
		}
	});
});