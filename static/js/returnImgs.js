
function loadImgs(){

    var imagenesSecundarias = document.getElementById("imagenesSecundarias");
    var imagenPrincipal = document.getElementById("imagenPrincipal");
    var filenames = document.getElementById("filenameArray").innerHTML;

    

    var fnames = filenames.split(",");
    alert(fnames);
    for (var i = 0; i <= fnames.length - 1; i++){
        fnames[i] = fnames[i].split("'")[1];
    }

    imagenPrincipal.src = "..\\..\\static\\results\\" + fnames[0];

    for (var i = 1; i <= fnames.length - 1; i++){
        var thumb = document.createElement("img");
        thumb.src = "..\\..\\static\\results\\" + fnames[i];
        thumb.alt = "Image " + i;
        thumb.classList.add("thumb");
        imagenesSecundarias.appendChild(thumb);
    }

    
    

}
