/**
 * GoogleMapの表示
 */
var loadGMap = function(id, option){
  /**
   * マーカーのクリックイベントリスナーの登録
   */
  var setMarkerClickListener = function(marker, markerData) {
    google.maps.event.addListener(marker, 'click', function(event) {
      if (openInfoWindow) {
        openInfoWindow.close();
      }
      openInfoWindow = new google.maps.InfoWindow({
        content: markerData.content
      });
      google.maps.event.addListener(openInfoWindow,'closeclick',function(){
        openInfoWindow = null;
      })
      openInfoWindow.open(marker.getMap(), marker);
      
      $('#top-image-box').children("img").attr({'src': '/image?data_id='+markerData.id});
    });
  };
  
  /**
   * マーカーデータのセット
   */
  var setMarkerData = function(markerArray) {
    for (var i = 0; i < markerArray.length; i++) {
      var marker = new google.maps.Marker({
        position: markerArray[i].position,
        title: markerArray[i].title,
        map: gmap,
        icon: null,
        shadow: null
      });
      markers.push(marker) 
      setMarkerClickListener(marker, markerArray[i], true);
    }
  }; 
 
  /**
   * マーカー削除
   */
  var clearMarkerData = function(){
    var i;
    if(markers.length > 0){
      for ( i = 0; i <  markers.length; i++) {
        markers[i].setMap(null);
      }
      markers.length = 0;
    }
  }
    
  /**
   * マーカーのリフレッシュ 
   */
  var refleshMarker = function(){
    clearMarkerData();
    
    //国土数値情報データ
    var data = $("#select_data").val()
    
    //地図の表示範囲を取得
    var bounds = gmap.getBounds();
    var northEastLatLng = bounds.getNorthEast();
    var southWestLatLng = bounds.getSouthWest();

    //国土数値情報の照会
    $.ajax({
      url: '/geo/find?data_class='+data+'&ne='+northEastLatLng.lat()+','+northEastLatLng.lng()+'&sw='+southWestLatLng.lat()+','+southWestLatLng.lng(),
      type: 'GET',
      dataType: 'json',
      timeout: 1000,
      error: function(){
        alert("地図データの読み込みに失敗しました");
      },
      success: function(json){
        var markerData = new Array();
        $.each(json.ResultSet,function(){
          markerData.push({
            position: new google.maps.LatLng(this.geo.coordinates[1], this.geo.coordinates[0]), 
            id: this._id,
            title: this.name,
            content:this.name
          });
        });
      
        if(markerData){
          setMarkerData(markerData);
        }      
      }
    });    
  }
 
  option = option ? option : {};
  if(id == null){
    return;
  }
  var mapOption = {
    zoom: option.zoom || 16,
    center:option.center || new google.maps.LatLng(34.777276, 138.014444),
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    navigationControlOptions: {
      style: google.maps.NavigationControlStyle.DEFAULT
    }
  };
  
  var gmap = new google.maps.Map(document.getElementById(id), mapOption);

  var openInfoWindow;  
  
  var markers = new Array();

  // 地図変更時のリスナーの追加
  google.maps.event.addListener(gmap, 'idle', function(){
    refleshMarker();
  })

  // 表示国土数値情報データの変更イベントリスナー
  $(function() {
    $("select#select_ksj").change(function() {
      refleshMarker()
    });
  });
}
