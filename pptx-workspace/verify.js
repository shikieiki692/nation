const PptxGenJS = require('pptxgenjs');
const pptx = new PptxGenJS();

pptx.load('C:\\Obsidion\\妙妙屋\\pptx-workspace\\酸碱理论-提高班.pptx').then(() => {
    console.log('Slides:', pptx.slides.length);
    pptx.slides.forEach((slide, i) => {
        console.log(`Slide ${i + 1}:`, slide.data ? slide.data.length : 'N/A', 'objects');
    });
}).catch(err => {
    console.error('Error:', err.message);
});
