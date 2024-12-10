let dataTable;
const totalFiles = 11;

const formatter = new Intl.NumberFormat("vi-VN", {
  style: "currency",
  currency: "VND",
});

function initializeDataTable() {
  dataTable = $("#dataTable").DataTable({
    responsive: true,
    columns: [
      { data: "date" },
      { data: "no" },
      { data: "amount" },
      { data: "detail" },
    ],
    columnDefs: [
      {
        targets: 2,
        render: function (data, type, row) {
          if (type === "display") {
            const formatAm = formatter.format(data);

            if (data == $("#searchInput").val())
              return `<span class="bg-yellow-300 text-slate-800">${formatAm}</span>`;

            return formatAm;
          }
          return data;
        },
      },
      { className: "border-b border-slate-200 text-sm", targets: "_all" },
    ],

    pageLength: 40,
    lengthMenu: [],
    bLengthChange: false,
    bInfo: false,
    language: {
      url: "https://cdn.datatables.net/plug-ins/1.11.5/i18n/vi.json",
    },
    processing: true,
    deferRender: true,
    scrollY: 400,
    dom: '<"flex justify-between items-center max-lg:flex-wrap"l<"ml-2 max-lg:ml-0"i>>rtip',
    bPaginate: false,
    rowCallback: function (row, data, index) {
      $(row).addClass(
        "hover:bg-slate-100 transition-colors duration-200 text-slate-700"
      );
    },
    drawCallback: function () {
      $(".dataTables_paginate")
        .addClass("mt-4 flex justify-center")
        .find(".paginate_button")
        .addClass(
          "px-3 py-1 bg-white border border-slate-300 text-slate-500 hover:bg-slate-100"
        )
        .filter(".current")
        .addClass("bg-blue-500 text-white hover:bg-blue-600")
        .removeClass("bg-white text-slate-500");

      $(".dataTables_info").addClass("text-sm text-slate-700");

      $(".dataTables_length select").addClass(
        "ml-1 mr-1 py-1 px-2 border border-slate-300 rounded-md"
      );

      var next_cursor = localStorage.getItem("next-cursor");
      if (next_cursor != "null" && next_cursor != 0) {
        $("#next").removeClass("cursor-not-allowed");
        $("#next").removeAttr("disabled");
      } else {
        $("#next").addClass("cursor-not-allowed");
        $("#next").attr("disabled", "disabled");
      }

      var prev_cursor_list = JSON.parse(localStorage.getItem("prev-cursor"));
      if (prev_cursor_list.length != 0) {
        $("#prev").removeClass("cursor-not-allowed");
        $("#prev").removeAttr("disabled");
      } else {
        $("#prev").addClass("cursor-not-allowed");
        $("#prev").attr("disabled", "disabled");
      }
    },
  });
}

async function searchData(next_cursor) {
  $("#loading").show();
  dataTable.clear();
  //   const regex = new RegExp(`(${removeVietnameseTones(query)})`, "gi");

  var searchMoney = $("#seachMoney").val();
  var searchMessage = removeVietnameseTones($("#searchInput").val());

  const response = await fetch(
    `http://localhost:8000/query?amount=${searchMoney}&message=${searchMessage}&next_cursor=${next_cursor}`
  );

  const responseData = await response.json();
  console.log(responseData);
  var filteredData = responseData["data"]
    .filter((item) =>
      Object.values(item).some((value, index) => {
        if (index == 2) value = parseFloat(value.replace(/,/g, ""));
        return value.toString().toLowerCase();
      })
    )
    .map((item) => {
      return {
        date: item["date"],
        no: item["transactionId"],
        amount: item["credit"],
        detail: item["detail"],
      };
    });

  localStorage.setItem("next-cursor", responseData["next_cursor"]);
  localStorage.setItem("current-cursor", next_cursor);

  dataTable.rows.add(filteredData).draw(false);

  $("#loading").hide();
}

$(document).ready(function () {
  initializeDataTable();

  resetLocalStorage();

  $("#searchButton").on("click", function () {
    resetLocalStorage();
    var next_cursor = localStorage.getItem("next-cursor");
    searchData(next_cursor);
  });

  $("#searchInput").on("keypress", function (e) {
    if (e.which === 13) {
      $("#searchButton").click();
    }
  });

  $("#next").on("click", function () {
    var next_cursor = localStorage.getItem("next-cursor");
    var current_cursor = localStorage.getItem("current-cursor");
    searchData(next_cursor);
    var prev_cursor_list = JSON.parse(localStorage.getItem("prev-cursor"));
    prev_cursor_list.push(current_cursor);
    localStorage.setItem("prev-cursor", JSON.stringify(prev_cursor_list));
  });

  $("#prev").on("click", function () {
    var prev_cursor_list = JSON.parse(localStorage.getItem("prev-cursor"));
    var prev_page_cursor = prev_cursor_list[prev_cursor_list.length - 1];
    searchData(prev_page_cursor);

    prev_cursor_list.pop();
    localStorage.setItem("prev-cursor", JSON.stringify(prev_cursor_list));
  });
});

function removeVietnameseTones(str) {
  str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, "a");
  str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, "e");
  str = str.replace(/ì|í|ị|ỉ|ĩ/g, "i");
  str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, "o");
  str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, "u");
  str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, "y");
  str = str.replace(/đ/g, "d");
  str = str.replace(/À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ/g, "A");
  str = str.replace(/È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ/g, "E");
  str = str.replace(/Ì|Í|Ị|Ỉ|Ĩ/g, "I");
  str = str.replace(/Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ/g, "O");
  str = str.replace(/Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ/g, "U");
  str = str.replace(/Ỳ|Ý|Ỵ|Ỷ|Ỹ/g, "Y");
  str = str.replace(/Đ/g, "D");
  // Some system encode vietnamese combining accent as individual utf-8 characters
  // Một vài bộ encode coi các dấu mũ, dấu chữ như một kí tự riêng biệt nên thêm hai dòng này
  str = str.replace(/\u0300|\u0301|\u0303|\u0309|\u0323/g, ""); // ̀ ́ ̃ ̉ ̣  huyền, sắc, ngã, hỏi, nặng
  str = str.replace(/\u02C6|\u0306|\u031B/g, ""); // ˆ ̆ ̛  Â, Ê, Ă, Ơ, Ư
  // Remove extra spaces
  // Bỏ các khoảng trắng liền nhau
  str = str.replace(/ + /g, " ");
  str = str.trim();
  // Remove punctuations
  // Bỏ dấu câu, kí tự đặc biệt
  // str = str.replace(/!|@|%|\^|\*|\(|\)|\+|\=|\<|\>|\?|\/|,|\.|\:|\;|\'|\"|\&|\#|\[|\]|~|\$|_|`|-|{|}|\||\\/g," ");
  return str;
}

function resetLocalStorage() {
  /** Clear Local Storage and set null for all cursor */
  localStorage.setItem("prev-cursor", JSON.stringify([]));
  localStorage.setItem("current-cursor", 0);
  localStorage.setItem("next-cursor", 0);
}
