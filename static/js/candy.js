async function loadImage(imgId) {
            try {
                const response = await fetch('/get-image/' + imgId);
                if (response.ok) {
                    const blob = await response.blob();
                    const img = document.getElementById('async-image-' + imgId);
                    img.src = URL.createObjectURL(blob);
                } else {
                    console.error('Failed to fetch image' + imgId);
                }
            } catch (error) {
                console.error('Failed to fetch image' + imgId, error);
            }
        }



        window.onload = loadAllImages;