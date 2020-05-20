$(() => {
    // v2rayHas ?
    $.get('/v2rayHas', {}, (res) => {
        if (res['code'] == 0) 
            console.log('检查出错')
        else {
            $('#V2rayCorePath').val(res['data']['v2ray']['V2rayCorePath'])
            $('#V2rayLogPath').val(res['data']['v2ray']['V2rayLogPath'])
            $('#loglevel').text(res['data']['v2ray']['LogLevel'])
            $('#Port').val(res['data']['v2ray']['Port'])
            $('#Portocol').text(res['data']['v2ray']['Portocol'])
            $('#UUID').val(res['data']['v2ray']['UUID'])
            $('#Data_portocol').text(res['data']['v2ray']['DataPortocol'])
        }
    })

    // 绑定下拉列表点击事件
    var dropdownitem = $('a.dropdown-item')
    for (var i = 0; i < dropdownitem.length; i++) {
        $(dropdownitem[i]).click(function() {
            droplistselected(this)
        })
    }

    $('#UuidUpdate').click(() => {
        updateUUID()
    })

    $('#SubmitConfig').click(() => {
        if ($('#Data_portocol').text().replace(/\n/g, '').replace(/ /g, '') === "Shadowsocks")
            updateShadowsocks()
        updateConfig()
    })
})

function droplistselected(t) {
    value = $(t).text()
    button = $(t).parent().parent().children()[0]
    $(button).text(value)
}

function updateUUID() {
    $.get('/updateUUID', {}, (res) => {
        if (res['code'] == 0)
            alert('无法获取UUID')
        else {
            $('#UUID').val(res['data']['uuid'])
        }
    })
}

function updateConfig() {
    $.get('/updateConfig', {
        V2rayCorePath   : $('#V2rayCorePath').val(),
        V2rayLogPath    : $('#V2rayLogPath').val(),
        LogLevel        : $('#loglevel').text().replace(/\n/g, '').replace(/ /g, ''),
        Port            : $('#Port').val(),
        Portocol        : $('#Portocol').text().replace(/\n/g, '').replace(/ /g, ''),
        UUID            : $('#UUID').val(),
        DataPortocol    : $('#Data_portocol').text().replace(/\n/g, '').replace(/ /g, ''),
    }, (res) => {
        console.log(res)
    })
}

function updateShadowsocks() {
    $.get('/updateShadowsocks', {
        ShadowsocksID   : $('#ShadowsocksID').val(),
        ShadowsocksPwd  : $('#ShadowsocksPwd').val()
    }, (res) => {
        console.log(res)
    })
}

function ShadowsocksConfig(t) {
    if ($(t).text() === "Vmess")
        $('#Shadowsocks').fadeOut('fast')
    else 
        $('#Shadowsocks').fadeIn('fast')
}