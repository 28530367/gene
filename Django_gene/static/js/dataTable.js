$(document).ready(function(){
    var table = $('#DataTable').DataTable(
        {
            processing: true,
            serverSide: true,
            language: {
                searchPlaceholder: "Please Press Enter."
            },
            searching: false,

            ajax: {
                "url": "/update_GeneAnnotation/",
                "type": "GET"
            },
            columns: [
                {data: 'Gene ID', title: 'Gene ID', orderable: true},
                {data: 'Gene location', title: 'Gene location', orderable: true},
                {data: 'Gene expression', title: 'Gene Expression'},
                {data: 'Accession number (Best hits in the GenBank)', title: 'Accession number (Best hits in the GeneBank)', orderable: true},
                {data: 'Annotation', title: 'Annotation', orderable: true},
                {data: 'Species', title: 'Species', orderable: true},
                {data: 'Blast Score', title: 'Blast Score', orderable: true},
                {data: 'Expect value', title: 'Expect value', orderable: true},
                {data: 'Identities', title: 'Identities', orderable: true},
                {data: 'Frame', title: 'Frame', orderable: true},
                {data: 'KEGG pathway', title: 'KEGG pathway', orderable: true},
                {data: 'GO Term', title: 'GO Term', orderable: true},
                {data: 'Interpro', title: 'Interpro', orderable: true},
                {data: 'Pfam', title: 'Pfam'},
                {data: 'Swissprot', title: 'Swissprot', orderable: true},
                {data: 'TrEMBL', title: 'TrEMBL', orderable: true},
                {data: 'TF_ath', title: 'Potential Transcription factor <br>(<I>A. thaliana</I>)', orderable: true},
                {data: 'TF_osa', title: 'Potential Transcription factor <br>(<I>O. sativa</I>)', orderable: true},
            ],
            "scrollX": true,
            "deferRender": true,
            'dom': '<"top"frB>t<"bottom"lrip>',
        });
})

