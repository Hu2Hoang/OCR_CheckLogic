const request = require('request');
const fs = require("fs");

// const filePath = './pdf/2318 GDSC-PTIT Ban cam ket 1.pdf';
// const file = fs.readFileSync(filePath);


// const data = {
//     requests: [
//       {
//         inputConfig: { content: Buffer.from(file).toString("base64") , mimeType: 'application/pdf' },
//         features: [
//           {
//             type: "DOCUMENT_TEXT_DETECTION",
//           },
//         ]
//       },
//     ],
// };

// request.post({
//     headers: {'content-type' : 'application/json'},
//     url: `https://vision.googleapis.com/v1/files:annotate?key=${KEY}`,
//     json: data
// }, function(error, response, body){
//     if (error) {
//         console.error('Error:', error);
//         return;
//     }

//     // Assuming the response body contains text data in fullTextAnnotation
//     if (body.responses && body.responses[0] && body.responses[0].fullTextAnnotation) {
//         const text = body.responses[0].fullTextAnnotation.text;
//         fs.writeFileSync('response.txt', text);
//         console.log('Response saved to response.txt');
//     } else {
//         console.log("No text data found in the response.");
//     }
// });

const filePath = './sodo.jpg';
const fileBase64 = fs.readFileSync(filePath, {encoding: 'base64'});


const data = {
    requests: [
      {
        image: { content: fileBase64 },
        features: [
          {
            type: "DOCUMENT_TEXT_DETECTION",
          },
        ],
      },
    ],
};
request.post({
    headers: {'content-type' : 'application/json'},
    url: `https://vision.googleapis.com/v1/images:annotate?key=${KEY}`,
    json: data
}, function(error, response, body){
    if (error) {
        console.error('Error:', error);
        return;
    }

    // Extract and display the text data
    if (body.responses && body.responses[0] && body.responses[0].fullTextAnnotation) {
        const text = body.responses[0].fullTextAnnotation.text;
        console.log(text);
    } else {
        console.log("No text data found in the response.");
    }
});
