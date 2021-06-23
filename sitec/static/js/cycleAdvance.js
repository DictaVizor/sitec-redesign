$(window).on('load', function(){
    let subjectData
    let panelData
    //Subject units 8 max??
    const NUMBER_CLASS_NAME = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight'
    }

    let COLORS = ['blue', 'red', 'orange', 'violet', 'teal', 'olive', 'purple', 'brown', 'pink']


    let cycleAdvanceContainer = $('#cycle-advance-container')
    let studentDataContainer = $('#student-data-container')
    let exportScoresButton = $('button#export-scores')
    let exportScheduleButton = $('button#export-schedule')


    exportScoresButton.on('click', exportScores)
    exportScheduleButton.on('click', exportSchedule)


    cycleAdvanceContainer.api({
        on: 'now',
        action: 'get user profile',
        beforeXHR: suiSetRequestHeaders,
        onSuccess: function(response){
            subjectData = response.sitec_data.cycle_advance_data
            panelData = response.sitec_data.panel_data
            console.log(response.sitec_data.kardex_data)
            let studentData = response.sitec_data.panel_data
            $.each(subjectData, function(i, subject){
                let _subject = subjectTemplate(subject)
                cycleAdvanceContainer.append(_subject)
            })

            studentDataContainer.prepend(studentDataTemplate(studentData))

        }
    })






    function studentDataTemplate(data){
        let student = $(`
        <h3 class="ui header">
            ${data['current-period'].value}
         </h3>
        `)

        student.data = data
        return student
    }

    function subjectTemplate(data){
        let random = Math.floor(Math.random() * COLORS.length)
        let subject = $(`
            <div class="ui ${COLORS[random]} secondary inverted segment">
                <h3 class="ui header">
                <div class="content">
                    <strong>${data.name}</strong>
                        <div class="sub header">
                            ${data.title}
                        </div>
                    </div>
                </h3>  
                <div class="ui basic segment">
                    <div class="ui grid">
                        <div class="${NUMBER_CLASS_NAME[data.units.length]} column center aligned row unit headers">

                        </div>
                        <div class="sixteen wide column no padding">
                            <div class="ui inner segment">
                                <div class="ui grid">
                                    <div class="${NUMBER_CLASS_NAME[data.units.length]} column center aligned row unit scores">
                                            
                                    </div>
                                </div>
                                <div class="ui grid">
                                    <div class="${NUMBER_CLASS_NAME[data.units.length]} column center aligned row unit misses">
                                        
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `)


        //add units
        $.each(data.units, function(i, unit){
            subject.find('.unit.headers').append(`
                <div class="column">
                    <span class="ui white text">U${unit.number+1}</span>
                </div>
            `)
            subject.find('.unit.scores').append(`
                <div class="ui column">
                <div class="ui white label">
                    ${unit.score}
                    </div>
                </div>
            `)
            subject.find('.unit.misses').append(`
                <div class="column">
                    <span class="ui small text">Faltas: ${unit.missed_days}</span>
                </div>
            `)
        })

        subject.data = data

        COLORS.splice($.inArray(COLORS[random], COLORS), 1)

        return subject
    }

    function exportSchedule(){
        console.log('Export Schedule!')
    }

    function exportScores(){
        let columns = [['Materia', 'Docente', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6']]
        let rows = []
        $.each(subjectData, function(i, subject){
            let rowData = [
                subject.name  + ' - ' + subject.title.split('–')[0],
                subject.title.split('–')[1].replace('�', 'Ñ')
            ]



            $.each(subject.units, function(i, unit){
                rowData.push(100)
            })
            rows.push(rowData)
        })
        var doc = new jsPDF('p', 'pt')
        doc.addImage(logos, 0, 10)
        doc.setFontSize(22)
        doc.text('Avance del ciclo', 20, 130)
        doc.setFontSize(16)
        doc.text(panelData.name, 20, 150)
        doc.text(`${panelData.control_number} - ${panelData['current-period'].value}`, 20, 170)
        doc.setFontSize(11)
        doc.text(doc.splitTextToSize('A continuación se muestran las materias que fueron cargadas y las evaluaciones correspondientes por unidades para el presente ciclo. La columna REP indica si la materia fue cargada por reprobación o curso espacial. U01 indica la calificación para la unidad 1 de la materia y así sucesivamente. Opción es el tipo de evaluación de la unidad NP: No Presentó, ORD: Ordinario/Normal, REG: Regularización y EXT: Extraordinario. Prom Est es el promedio estimado en la materia para el alumno y solo el que se muestra en el Kardex es el definitivo. Si existe alguna duda sobre la presente información verifícalo con el maestro o el coordinador de carrera.', 550), 20, 190)
        doc.autoTable({
            theme: 'grid',
            headStyles: { fillColor: [0,123,255] },
            head: columns,
            body: rows,
            margin: {
                top: 280,
                left: 20,
            }
        })
        doc.save('calificaciones.pdf')
    }

})