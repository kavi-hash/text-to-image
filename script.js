document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#prompt_bar');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(form);
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const imageBlob = await response.blob();
            const imgElement = document.createElement('img');
            imgElement.src = URL.createObjectURL(imageBlob);
            
            const imgBox = document.createElement('div');
            imgBox.className = 'img_box';
            imgBox.appendChild(imgElement);
            
            const imageResult = document.getElementById('image_result');
            imageResult.innerHTML = ''; // Clear previous images
            imageResult.appendChild(imgBox);
        } else {
            console.error('Error generating image');
        }
    });
});
