const imgInput = document.getElementById('id_img');
const imgPreview = document.getElementById('img-preview');

imgInput.addEventListener('change', function(event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            imgPreview.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }
});