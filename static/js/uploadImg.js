const form = document.getElementById("myForm");
const loader = document.getElementById("loader");

form.addEventListener("submit", function(event) {
    form.style.display = "none";
    loader.style.display = "block";
});

function FileDetails() {
    // GET THE FILE INPUT.
    var f = document.getElementById('files');

    // VALIDATE OR CHECK IF ANY FILE IS SELECTED.
    if (f.files.length > 0) {
        // RUN A LOOP TO CHECK EACH SELECTED FILE.
        for (var i = 0; i <= f.files.length - 1; i++) {
                
            var fname = f.files.item(i).name;      // THE NAME OF THE FILE.
            extension = fname.split('.').pop();      // THE EXTENSION OF THE FILE.

            if(extension == "png" || extension == "jpg" || extension == "jpeg"){
                if(f.files.length == 1){
                    document.getElementById('text').innerHTML = 'Has seleccionado: <b>' + f.files.length + ' imágen.';
                }else{
                    document.getElementById('text').innerHTML = 'Has seleccionado: <b>' + f.files.length + ' imágenes.';
                } 
                document.getElementById("submit").style.opacity = 1;
                document.getElementById("submit").disabled = false;
                document.getElementById("text").style.color = 'black';

            }else{
                document.getElementById('text').innerHTML = 'Formato de archivo incorrecto';
                document.getElementById("text").style.color = 'red';
                document.getElementById("submit").disabled = true;
            }
        }
    }
    else { 
        alert('Please select a file.') 
    }
}