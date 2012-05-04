package com.memorykloud.Activities;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;

import com.memorykloud.R;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.GridView;

import com.memorykloud.Adapters.*;
import com.memorykloud.Adapters.KloudletAdapter.ViewHolder;
import com.memorykloud.Http.HttpPackage;
import com.memorykloud.Http.HttpRequestTask;
import com.memorykloud.Http.IHttpCallback;
import com.memorykloud.Sat.*;
import com.memorykloud.Sat.SatelliteMenu.SateliteClickedListener;
import com.memorykloud.Sat.SatelliteMenuItem;

public class KloudletViewerActivity extends Activity implements
IHttpCallback<Void>{

	protected String _url_get_kloudlets_by_user;
	private HttpRequestTask _httpTask;
	private KloudletAdapter _adap;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.mk_kloudlet_viewer);

		InitializePage();
	}

	/** Called when the page is initialized **/
	private void InitializePage() {
		/* Variable Configuration */
		_url_get_kloudlets_by_user = this
				.getString(R.string.URL_GET_KlOUDLETS);

		/* UI Configuration */
		InitializeSatelliteMenu();

		/* HTTP queries */
		GetKloudletsByUserId();
	}

	private void InitializeSatelliteMenu() {
		SatelliteMenu menu = (SatelliteMenu) findViewById(R.id.menu);
		float distance = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP,
				200, getResources().getDisplayMetrics());
		menu.setSatelliteDistance((int) distance);
		menu.setExpandDuration(500);
		menu.setCloseItemsOnClick(true);
		menu.setTotalSpacingDegree(90);

		List<SatelliteMenuItem> items = new ArrayList<SatelliteMenuItem>();
		items.add(new SatelliteMenuItem(6, R.drawable.menu_friend));
		items.add(new SatelliteMenuItem(5, R.drawable.menu_location));
		items.add(new SatelliteMenuItem(4, R.drawable.menu_audio));
		items.add(new SatelliteMenuItem(3, R.drawable.menu_thought));
		items.add(new SatelliteMenuItem(2, R.drawable.menu_pic));
		items.add(new SatelliteMenuItem(1, R.drawable.menu_kloudlet));
		menu.addItems(items);

		menu.setOnItemClickedListener(new SateliteClickedListener() {

			public void eventOccured(int id) {
				switch (id) {
				case 1: // kloudlet
					startActivity(new Intent(KloudletViewerActivity.this,
							KloudletManagerActivity.class));
					break;
				case 2: // picture
					break;
				case 3: // thought
					break;
				case 4: // audio
					break;
				case 5: // location
					break;
				case 6: // friend
					break;
				}
			}
		});
	}
	
	private void GetKloudletsByUserId() {
		// populate the kloudlets list based on the given user
		// TODO: For now, we assume the all kloudlets being pulled out

		this._httpTask = new HttpRequestTask(this, this,
				HttpRequestTask.HTTPType.GET);
		List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
		nameValuePairs.add(new BasicNameValuePair("id", "all"));
		nameValuePairs.add(new BasicNameValuePair("showcover", "true"));

		this._httpTask.SetPackage(_url_get_kloudlets_by_user,
				new HttpPackage(_url_get_kloudlets_by_user, nameValuePairs));
		_httpTask.execute();
	}

	@Override
	public void onHttpTaskComplete(Void noParams) {
		HttpPackage pkg = null;
		Object result = null;
		pkg = this._httpTask.GetPackage(_url_get_kloudlets_by_user);
		if (pkg != null) {
			result = pkg.get_response();
			if (result != null) {
				if (result instanceof JSONArray) {				
					// create an adapter
					_adap = new KloudletAdapter(this);
					// get the moments and fill in the adapter
					JSONArray jArray = (JSONArray) result;
					_adap.SetJSONArray(jArray);

					// attach the events with the gridview
					GridView gridview = (GridView) findViewById(R.id.gridview);
					gridview.setAdapter(_adap);					
					gridview.setOnItemClickListener(new OnItemClickListener() {
						@Override
						public void onItemClick(AdapterView<?> parent, View v,
								int position, long id) {
							ViewHolder holder = (ViewHolder) v.getTag();
							
							// pass along the data for the next invoked activity
							Bundle bundle = new Bundle();
							bundle.putInt("kloudlet_id", holder.getKloudlet_Id());
							bundle.putString("kloudlet_name", holder.getKloudlet_Name().getText().toString());

							Intent intent = new Intent(KloudletViewerActivity.this,
									MomentViewerActivity.class);
							intent.putExtras(bundle);
							startActivity(intent);
						}
					});	
				}
			}
		}

		this._httpTask.ClearPackage();
		
	}
	
	public void Settings_Click(View view){
		startActivity(new Intent(KloudletViewerActivity.this,
				SettingsActivity.class));
    } 
}
