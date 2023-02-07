
function loadImgs(){

    var imagenesSecundarias = document.getElementById("imagenesSecundarias");
    var imagenPrincipal = document.getElementById("imagenPrincipal");
    var filenames = document.getElementById("filenameArray").innerHTML;

    var fnames = filenames.split(",");
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
    thumbs = document.getElementsByClassName("thumb");
    
    //for every element with class "thumb" add an onclick event that changes the src of the main image
    for (var i = 0; i < thumbs.length; i++) {
        thumbs[i].addEventListener("click", function(){
            imagenSecundaria = this.src;
            this.src = imagenPrincipal.src;
            imagenPrincipal.src = imagenSecundaria;
        });
    }
}