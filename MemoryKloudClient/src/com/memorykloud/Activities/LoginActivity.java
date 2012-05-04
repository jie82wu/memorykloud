package com.memorykloud.Activities;

import org.json.JSONArray;

import com.memorykloud.R;

import com.memorykloud.Adapters.MomentAdapter;
import com.memorykloud.Http.HttpPackage;
import com.memorykloud.Http.HttpRequestTask;
import com.memorykloud.Http.IHttpCallback;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;


public class LoginActivity extends Activity implements
		IHttpCallback<Void> {

	public ProgressDialog _progressDialog;
	private EditText _userEditText;
	private EditText _passwordEditText;
	private HttpRequestTask _httpTask;
	
	/**
	 * Called when the activity is first created. This is the entry point for
	 * our MemoryKloud application
	 */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.mk_login);

		InitializePage();
	}
	private void InitializePage(){
		// Variable Initialization
		
		
		// UI
		_progressDialog = new ProgressDialog(this);
		_progressDialog.setMessage("Please wait...");
		_progressDialog.setIndeterminate(true);
		_progressDialog.setCancelable(false);
		_userEditText = (EditText) findViewById(R.id.Username);
		_passwordEditText = (EditText) findViewById(R.id.Password);
	}

	public void SignIn_Click(View view) {
		int usersize = _userEditText.getText().length();
		int passsize = _passwordEditText.getText().length();
		if (usersize > 0 && passsize > 0) {
			_progressDialog.show();
			/*
			 * Login logic comes in String user =
			 * UserEditText.getText().toString(); String pass =
			 * PassEditText.getText().toString(); doLogin(user, pass);
			 */

			_progressDialog.dismiss();

			/* launch the EventViewer screen */
			startActivity(new Intent(LoginActivity.this,
					KloudletViewerActivity.class));

		} else
			createDialog("Sorry", "Please enter Username and Password");
	}

	public void SignUp_Click(View view) {
		// Example of running back-end HTTP requests
		this._httpTask = new HttpRequestTask(this, this, HttpRequestTask.HTTPType.GET);
		this._httpTask.SetPackage("InternetTest", new HttpPackage("http://www.google.com"));
		_httpTask.execute();
	}

	public void createDialog(String title, String text) {
		AlertDialog ad = new AlertDialog.Builder(this)
				.setPositiveButton("Ok", null).setTitle(title).setMessage(text)
				.create();
		ad.show();
	}

	@Override
	public void onHttpTaskComplete(Void noParams) {
		HttpPackage pkg= null;
		Object result = null;
		pkg = this._httpTask.GetPackage("InternetTest");
		if (pkg != null ){
			result = pkg.get_response();
			if (result != null) {
				if (result instanceof String) {
					createDialog("hello", result.toString());
					}
			}
		}
		
		this._httpTask.ClearPackage();
	}
}