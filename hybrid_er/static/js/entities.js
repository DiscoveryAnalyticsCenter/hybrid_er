// const supportClusters[]

function format ( d ) {
    // `d` is the original data object for the row
    // const data = supportClusters[d[1]];
    const data = [
      {score: 0.8922, cluster: 1, text: '"the university of waterloo", "university of waterloo cheriton", "university of waterloo", "mila university of waterloo", "waterloo university", "simons institute and university of waterloo", "univ of waterloo"'},
      {score: 0.7811, cluster: 857, text: '"university of washington university of washington northeastern university university of washington", "university of washington box", "university of washington from", "university of washington", "university of washington university of washington", "washington state university", "the university of washington"'},
    ];

    let html = `<div><p>Choose a better cluster for <strong>${d[1]}</strong>:</p>
    <table class="innerTable" cellpadding="5" cellspacing="0" border="0" style="margin-bottom:50px">
    <thead>
      <td>Best</td>
      <td>Score</td>
      <td>Cluster</td>
    </thead><tbody>`;

    html = data.reduce((prev, cluster, i) => {
      return prev + `<tr>
        <td><input type="radio" name="recluster${d[6]}" id="recluster${d[6]}_${cluster.cluster}" value="${cluster.cluster}" ${i == 0 ? "checked" : ""}></td>
        <td>${cluster.score}</td>
        <td>${cluster.text.substring(0, 125)}...</td>
      </tr>`;
    }, html);

    return html + '</tbody></table></div';
}


$(document).ready( function () {
    // return;
    const table = $('#candidateTable').DataTable({
      paging: false,
      ordering: false,
      info: false,
      searching: false,
      columns: [
        {},
        {},
        {},
        {},
        {},
        {
          className: 'details-control',
          orderable: false,
          data: null,
          defaultContent: ''
        }
      ],
    });

    const junkyard = document.getElementById("hidden-forms");

    $(".has-radio").on("click", (event) => {
      const input = $(event.target).find('input');
      console.log("set input", input);
      input.prop("checked", true);
    });

    $(".canonical").on("click", (event) => {
      console.log("Canonical", event)
      $(".selected-row", $(event.target).parents('tbody')).toggleClass("selected-row");
      $(event.target).parents("tr").toggleClass("selected-row");
    });

    $(".tr-radio").on("click", (event) => {
      $(".selected-inner-row", $(event.target).parent().parent()).toggleClass("selected-inner-row");
      const tr = $(event.target).parent()
      tr.toggleClass("selected-inner-row");

      const input = $(event.target).parent().find("input");
      input.prop("checked", true);

      toggleDrawer(tr.parents('table').parents('tr').prev());
    });

    const toggleDrawer = function (tr) {
        var row = table.row( tr );
        const candidateID = tr.attr("data-candidate-pk");
        console.log("Opening row for", candidateID);

        if ( row.child.isShown() ) {
            // This row is already open - close it
            const html = document.getElementById(`candidate-clusters-${candidateID}`)
            junkyard.append(html);

            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            // const html = format(row.data());
            const html = document.getElementById(`candidate-clusters-${candidateID}`);
            row.child($(html)).show();
            tr.addClass('shown');
        }
    }

    $('.no-td').on('click', function() {
      const tr = $(this).closest('tr');
      toggleDrawer(tr);
    });
    $('#candidateTable tbody').on('click', 'td.details-control', function() {
      const tr = $(this).closest('tr');
      toggleDrawer(tr);
    });
} );
