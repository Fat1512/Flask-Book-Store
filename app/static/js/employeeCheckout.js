function onScanSuccess(decodedText, decodedResult) {
    // handle the scanned code as you like, for example:
    console.log(`Code matched = ${decodedText}`, decodedResult);
    html5QrcodeScanner.pause(1);
    setTimeout(() => {
      html5QrcodeScanner.resume();
    }, 1000);
    //   alert(`Code matched = ${decodedText}`, decodedResult);
  }

  function onScanFailure(error) {
    // handle scan failure, usually better to ignore and keep scanning.
    // for example:
    //   console.warn(`Code scan error = ${error}`);
  }

  // const Html5QrcodeSupportedFormats = {
  //   EAN_13,
  // };

let html5QrcodeScanner = new Html5QrcodeScanner(
"reader",
{
    fps: 10,
    qrbox: { width: 400, height: 300 },
},
/* verbose= */ false
);
html5QrcodeScanner.render(onScanSuccess, onScanFailure);
