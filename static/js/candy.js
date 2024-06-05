async function loadImage(imgElement) {
    const imgId = imgElement.getAttribute('data-img-id');
    try {
        const response = await fetch(`/get-image/${imgId}`);
        if (response.ok) {
            const blob = await response.blob();
            imgElement.src = URL.createObjectURL(blob);
        } else {
            console.error(`Failed to fetch image ${imgId}`);
        }
    } catch (error) {
        console.error(`Error fetching image ${imgId}:`, error);
    }
}

function loadAllImages() {
    const images = document.querySelectorAll('.async-image');
    images.forEach(imgElement => loadImage(imgElement));
    window.scrollTo(0, document.body.scrollHeight);
}

window.onload = loadAllImages;
