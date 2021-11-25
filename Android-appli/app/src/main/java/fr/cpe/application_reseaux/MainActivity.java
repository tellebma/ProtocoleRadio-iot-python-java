package fr.cpe.application_reseaux;

import androidx.appcompat.app.AppCompatActivity;


import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;

public class MainActivity extends AppCompatActivity {

    /* Mise en place des variables utilisées par l'application*/
    private EditText port; /* Variable qui définit le edittext contenant le numéro de port*/
    private EditText ip;/* Variable qui définit le edittext contenant l'IP'*/
    private Button bouton;/* Bouton de l'application permettant de changer l'ordre d'affichage des capteurs*/
    private Button connect;/*Bouton pour initialisé ou modifier la connexion avec les paramètres rentré en IP et Port*/
    private InetAddress address;/* Variable qui contient l'adresse IP au bon format */
    private DatagramSocket UDPSocket;/*Permet la connexion*/
    private TextView values;/*Variable utilisé pour l'affichage des capteurs*/
    private String state;/*Variable qui change de valeur lors de l'appuie sur "bouton" dans l'objectif de changer l'ordre d'affichage*/
    private int int_port;/* Variable qui contient le port au bon format */
    private byte[] msg = new byte[2];/*Contient le message que l'on envoie à la passerelle*/
    private byte[] receive = new byte[50]; /* Contient les données envoyé par the passerelle */
    private int auth;/*Permet de vérifier que la connexion est établie pour éviter des crash de l'application */
    private String getst;
    private String[] split;
    private String result;

    @Override
    /*Exécuté au lancement de l'application*/
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        (new ReceiverTask()).execute();
        /*Initialisation des variables avec les données de la view*/
        port = findViewById(R.id.port);
        ip = findViewById(R.id.ip);
        bouton = findViewById(R.id.button);
        state = "TL";
        values = findViewById(R.id.values);
        connect = findViewById(R.id.connect);

        /*S'exécute lors d'un appui sur le bouton connect*/
        connect.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {

                try {
                    /*Initialisation de la connexion UDP*/
                    UDPSocket = new DatagramSocket();
                    String value = port.getText().toString();
                    int_port = Integer.parseInt(value);
                    address = InetAddress.getByName((ip.getText().toString()));
                    /*Passe à 1 quand une connexion a été initialisé avec des paramètres valides*/
                    auth = 1;
                } catch (IOException e) {
                    e.printStackTrace();
                }
                (new ReceiverTask()).execute();
            }

        });

        /*S'exécute lors d'un appui sur le bouton "bouton"*/
        bouton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                /*Permet de changer la variable state à chaque appui en vérifiant son état précédant*/
                if (state == "LT") {
                    state = "TL";
                    bouton.setText(R.string.temp);
                } else if (state == "TL") {
                    state = "LT";
                    bouton.setText(R.string.lumi);
                }
                msg = state.getBytes();
        /*On vérifie qu'un UDPSocket a été créé pour éviter un crash*/
                if (auth == 1) {
                    (new Thread() {
                        public void run() {
                            try {
                                DatagramPacket packet = new DatagramPacket(msg, msg.length, address, int_port);/*Préparation du paquet à envoyer*/
                                UDPSocket.send(packet);/*Envoie du paquet envoyé par la passerelle*/
                                getst = "getValues()";
                                sleep(2000);
                                msg = getst.getBytes();
                                DatagramPacket get = new DatagramPacket(msg, msg.length, address, int_port);/*Préparation du paquet à envoyer*/
                                UDPSocket.send(get);/*Envoie du paquet envoyé par la passerelle*/
                            } catch (IOException | InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                    }).start();
                } else {
                    /*Si aucune connection établie on écris une erreur*/
                    values.setText("Veuillez vous connectez");
                }

            }
        });
    }

    /*Executé en arrière plan sur un thread différent pour éviter de bloquer l'application*/
    private class ReceiverTask extends AsyncTask<Void, byte[], Void> {
        protected Void doInBackground(Void... rien) {
        if (auth==1) {
            try {
            while (true) {
                DatagramPacket packet = new DatagramPacket(receive, receive.length);/*Préparation du paquet à recevoir*/
                UDPSocket.receive(packet);/*Recepetion du paquet envoyé par la passerelle*/
                int size = packet.getLength();
                publishProgress(java.util.Arrays.copyOf(receive, size));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }}
        return null;
    }
    /*Executé en cas de reception*/
        protected void onProgressUpdate(byte[]... data) {
            values.setText("a");
            String str_receive = new String(receive, StandardCharsets.UTF_8);/*Conversion des bytes en chaîne de caractères*/
            split = str_receive.split(",");
            if (state == "LT"){
                result = "Luminosité : " + split[0] + ", Température : " + split[1];
            } else {
                result = "Température : " + split[0] + ", Luminosité : " + split[1];
            }
            values.setText(result);/*Affichage des valeurs*/
        }
    }
}
