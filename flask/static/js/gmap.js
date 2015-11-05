/**
 * GoogleMapの表示
 * @param {String} id 表示領域ID
 * @param {Object} option google.maps.Mapに設定するオプション
 * @param {Object} markerArray マーカーデータ配列
 * @param {Object} isNumberPin 番号付きマーカーで表示するか
 */
var loadGMap = function(id, option, markerArray){
  /**
   * マーカーのクリックイベントリスナーの登録
   * @param {google.maps.Marker} marker マーカーオブジェクト
   * @param {Object} markerData マーカーに設定する情報ウィンドウデータ
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
    });
  };
  
  /**
   * マーカーデータのセット
   * @param {Object} makerArray マーカーデータ
   */
  var setMarkerData = function(makerArray) {

    // 登録データ分のマーカーを作成
    for (var i = 0; i < makerArray.length; i++) {
      var marker = new google.maps.Marker({
        position: makerArray[i].position,
        title: makerArray[i].title,
        map: gmap,
        icon: null,
        shadow: null
      });

      // マーカーのclickリスナー登録
      setMarkerClickListener(marker, makerArray[i], true);
    }
  }; 
 
  /**
   * マーカー削除
   */
  var clearMarkerData = function(){
    var i;
    //表示中のマーカーがあれば削除
    if(markerArray.length > 0){
      //マーカー削除
      for ( i = 0; i <  markerArray.length; i++) {
        markerArray[i].setMap();
      }
      markerArray.length = 0;
    }
  }
    
  /**
   * マーカーのリフレッシュ 
   */
  var refleshMarker = function(){
    //リストの内容を削除
    $('#marker_list > ol').empty();
  
    //マーカー削除
    clearMarkerData();
    
    //地図の表示範囲を取得
    var bounds = gmap.getBounds();
    var northEastLatLng = bounds.getNorthEast();
    var southWestLatLng = bounds.getSouthWest();

    //jsonファイルの取得
    $.ajax({
      url: '/spot/find?ne='+northEastLatLng.lat()+','+northEastLatLng.lng()+'&sw='+southWestLatLng.lat()+','+southWestLatLng.lng(),
      type: 'GET',
      dataType: 'json',
      timeout: 1000,
      error: function(){
        alert("地図データの読み込みに失敗しました");
      },
      success: function(json){
        //帰ってきた地点の数だけループ
        var markerData = new Array();
        $.each(json.ResultSet,function(){
          markerData.push({
            position: new google.maps.LatLng(this.point.coordinates[1],this.point.coordinates[0]), 
            title: this.name,
            content:this.name
          });
        });
      
        // マーカーデータをセット
        if(markerArray){
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
  
  if(markerArray){
    setMarkerData(markerArray);
  }

  // 地図変更時のリスナーの追加
  google.maps.event.addListener(gmap, 'idle', function(){
    refleshMarker();
  })
}
