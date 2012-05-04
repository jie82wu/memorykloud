package com.memorykloud.Activities;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import com.memorykloud.R;
import com.memorykloud.Http.HttpPackage;
import com.memorykloud.Http.HttpRequestTask;
import com.memorykloud.Http.IHttpCallback;

public class KloudletManagerActivity extends Activity implements
		IHttpCallback<Void> {

	private HttpRequestTask _httpTask;
	protected String _url_post_create_kloudlet;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.mk_kloudletmgr);

		_url_post_create_kloudlet = this.getString(R.string.URL_POST_KLOUDLET);
	}

	public void SaveKloudlet_Click(View view) {

		// TODO: current UserId, hard code it for now
		int user_id = 882;

		EditText name = (EditText) findViewById(R.id.name);
		String kloudletName = name.getText().toString();

		EditText descp = (EditText) findViewById(R.id.description);
		String kloudletDescp = descp.getText().toString();

		CreateKloudlet(user_id, kloudletName, kloudletDescp);
	}

	private void CreateKloudlet(int uId, String name, String description) {
		// Create a moment with picture
		try {
			this._httpTask = new HttpRequestTask(this, this,
					HttpRequestTask.HTTPType.POST);

			List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
			nameValuePairs.add(new BasicNameValuePair("UID", "" + uId));
			nameValuePairs.add(new BasicNameValuePair("name", "" + name));

			this._httpTask.SetPackage(_url_post_create_kloudlet,
					new HttpPackage(_url_post_create_kloudlet, nameValuePairs));
			_httpTask.execute();

		} catch (Exception e) {
			// handle exception here
			Log.e(e.getClass().getName(), e.getMessage());
		}
	}

	@Override
	public void onHttpTaskComplete(Void noParams) {
		HttpPackage pkg = null;
		Object result = null;

		pkg = this._httpTask.GetPackage(_url_post_create_kloudlet);
		if (pkg != null) {
			result = pkg.get_response();
			if (result != null) {
				if (result instanceof String) {
					// For debugging purpose
					// Toast.makeText(MomentManagerActivity.this,
					// result.toString(), Toast.LENGTH_SHORT).show();
				}
				this.finish();
			}
		}

		this._httpTask.ClearPackage();

	}

	public void InviteFriends_Click(View view) {
		startActivity(new Intent(KloudletManagerActivity.this,
				FriendlistActivity.class));
	}
}
