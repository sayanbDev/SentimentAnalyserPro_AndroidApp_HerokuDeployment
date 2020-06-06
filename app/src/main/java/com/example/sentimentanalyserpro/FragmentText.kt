package com.example.sentimentanalyserpro

import android.annotation.SuppressLint
import android.os.AsyncTask
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import com.ibm.cloud.sdk.core.security.IamAuthenticator
import com.ibm.watson.natural_language_understanding.v1.NaturalLanguageUnderstanding
import com.ibm.watson.natural_language_understanding.v1.model.AnalyzeOptions
import com.ibm.watson.natural_language_understanding.v1.model.EntitiesOptions
import com.ibm.watson.natural_language_understanding.v1.model.Features
import com.ibm.watson.natural_language_understanding.v1.model.SentimentOptions
import kotlinx.android.synthetic.main.fragment_text.view.*

/**
 * A simple [Fragment] subclass.
 */
class FragmentText : Fragment() {

    @SuppressLint("SetTextI18n")
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view=inflater.inflate(R.layout.fragment_text, container, false)
        view.btnAnalyse.setOnClickListener {
            Log.i("MainActivity","trying to find the text's sentiment")
            Toast.makeText(activity,"Finding the text's sentiment",Toast.LENGTH_SHORT).show()
            var overallSentiment = "Positive"
            val authenticator = IamAuthenticator("ddW9L-8FFSnspXYJgnJiIzqp3FVnIatrW3irx3fEvkLr")
            var service = NaturalLanguageUnderstanding("2019-07-12", authenticator)
            service.serviceUrl="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/3528fc85-2e37-4554-ae6f-128c5927e415"
            val entities = EntitiesOptions.Builder().emotion(true)
                .sentiment(true)
                .limit(1L)
                .build()
            val sentimentOptions = SentimentOptions.Builder()
                .document(true)
                .build()
            val features: Features = Features.Builder()
                .entities(entities).sentiment(sentimentOptions)
                .build()
            val parameters: AnalyzeOptions = AnalyzeOptions.Builder().text(view.textToAnalyze.text.toString()).features(features).build()

            AsyncTask.execute {
                val results = service.analyze(parameters).execute()
                val c = results.result.sentiment.document.score
                if (c < 0.0)
                    overallSentiment = "Negative"
                if (c == 0.0)
                    overallSentiment = "Neutral"
                activity?.runOnUiThread {
                    view.txtView.text = "The text's sentiment is : $overallSentiment"
                }
            }
        }





        return view
    }

}
