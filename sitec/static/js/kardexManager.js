(function($){

    const COLORS = {
        'aprobada': 'inverted green',
        'pendiente': 'tertiary',
        'normal': '',
        'reprobada': 'inverted orange',
        'especial': 'inverted red',
        'sincursar': 'inverted secondary olive'
    }


    $.fn.kardexManager = function(settings){
        let self = this

        self.init = function(settings){
            self.settings = $.extend({}, settings, $.fn.kardexManager.settingsDefaults)
            self.subjects = []
            self.semesters = []
            self.loadData()
            self.semesterDropdown = self.find('.dropdown').dropdown({
                onChange: function(value){
                    self.filterSubjectsBySemester(value)
                }
            })

            return self
        }

        self.loadData = function(){
            self.api({
                on: 'now',
                action: 'get user profile',
                beforeXHR: suiSetRequestHeaders,
                onSuccess: function(response){
                    let data = response.sitec_data.kardex_data
                    self.processData(data)
                    self.trigger('data-loaded')
                },
                onError: function(){
                    //TODO: show error toast
                }
            })
        }

        self.processData = function(data){
            $.each(data, function(i, subject){
                self.addSubject(self.Subject(subject))
                self.semesters.push(subject.semester)
            })
            self.semesters = self.semesters.unique()
            self.initSemesterDropdown()
        }

        self.initSemesterDropdown = function(){
            $.each(self.semesters, function(i, semester){
                self.semesterDropdown.find('.menu').append(self.settings.semesterDropdownOptionTemplate(semester))
            })

            //Set selected not working. Manually setting value and text.
            self.semesterDropdown.dropdown('set value', 1)
            self.semesterDropdown.dropdown('set text', 'Semestre 1')

            self.find('.button.prev').on('click', function(){
                let currentSemester = parseInt(self.semesterDropdown.dropdown('get value'))

                if(currentSemester == 1){
                    currentSemester = self.semesters[self.semesters.length - 1] + 1
                }

                self.semesterDropdown.dropdown('set selected', currentSemester-1)
                
            })
            self.find('.button.next').on('click', function(){
                let currentSemester = parseInt(self.semesterDropdown.dropdown('get value'))

                if(currentSemester == self.semesters[self.semesters.length - 1]){
                    currentSemester = 0
                }

                self.semesterDropdown.dropdown('set selected', currentSemester+1)
            })
        }

        self.filterSubjectsBySemester = function(semester){
            $.each(self.subjects, function(i, subject){
                subject.toggle(subject.data.semester == semester)
            })
        }

        self.addSubject = function(subject){
            self.subjects.push(subject)
            self.find('.subject.segment').append(subject)
        }

        self.Subject = function(data){
            let subject = self.settings.subjectTemplate(data)

            subject.init = function(data){
                subject.data = data
                return subject
            }

            return subject.init(data)
        }

        return self.init(settings)
    }

    $.fn.kardexManager.settingsDefaults = {
        subjectTemplate: function(data){
            let segmentClass = COLORS[data.status]

            let segment = $(`
                <div class="ui ${segmentClass} clickable segment">
                    <h3 class="ui dividing header">
                        ${data.name}
                        <div class="sub header">
                            ${data.slug}
                        </div>
                    </h3>
                    <div class="ui inner basic segment">
                    </div>
                </div>
            `)
            let innerSegment = segment.find('.inner.segment')
            if('credits' in data){
                innerSegment.append(`<p>Creditos: ${data.credits}</p>`)
            }
            if('score' in data){
                innerSegment.append(`<p>Calificacion: ${data.score}</p>`)
            }
            if('tcs' in data){
                innerSegment.append(`<p>TC: ${data.tc}</p>`)
            }
            if('period' in data){
                innerSegment.append(`<p>Ciclo: ${data.period}</p>`)
            }
            if('taken_on' in data){
                innerSegment.append(`<p>Creditos: ${data.taken_on}</p>`)
            }
            return segment
        },
        semesterDropdownOptionTemplate: function(number){
            return $(`
            <div class="item" data-value="${number}">Semestre ${number}</div>
            `)
        }
    }

})(jQuery)