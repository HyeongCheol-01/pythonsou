// 함수(화살표함수) 객체 생성 후 $에 할당

const $ = (sel) => document.querySelector(sel);
//function $(sel){
//      return document.querySelector(sel);
//}
// ex) $("#sendBtn") 하면 document.querySelector(sel)가 실행

$("#sendBtn").addEventListener("click", async() => { //비동기 처리   
    const name = $("#name").value.trim()
    // const age = $("#age").value.trim()
    const age = document.querySelector("#age").value.trim();

    const params = new URLSearchParams({name, age}); // 공백 한글이 포함된 경우 자동 인코딩
    const url = `/api/friend?${params.toString()}`      // 최종 URL 생성 : /api/friend?name=길동&age=23

    $("#result").textContent = "요청 중...";    // 서버에 자료 요청 시간이 길어지면 보이는 메세지

    try{
        const res = await fetch(url,{
            method:"GET",
            headers:{"Accept":"application/json"}  // 응답 본문을 JSON으로 파싱해서 JS객체화
        });

        const data = await res.json();

        if (!res.ok || data.ok === false) {
            // 에러 메시지 출력 (닫는 태그 추가)
            $("#result").innerHTML = `<span style="color:red;">오류: ${data.error || '알 수 없는 에러'}</span>`;
        } else {
            // 성공 시 결과 출력
            $("#result").innerHTML = `
                <div style="margin-top: 20px; padding: 15px; border-radius: 8px; border: 1px solid #ddd; background-color: #fcfcfc;">
                    <p><strong>이름:</strong> ${data.name}</p>
                    <p><strong>나이:</strong> ${data.age}세</p>
                    <p><strong>연령대:</strong> ${data.age_group}</p>
                    <p style="color: blue; border-top: 1px dashed #ccc; pt-2;"><strong>메시지:</strong> ${data.message}</p>
                </div>
            `;
        }
    } catch (err) {
        $("#result").innerHTML = `<span class="error">네트워크/파싱 오류: ${err.message}</span>`;
    }
});
