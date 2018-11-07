<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:template match="/ligas">
        <html>
            <body>

                    <xsl:for-each select="liga">
                         <h1>
                             <xsl:value-of select="nomeliga"/>
                         </h1>
                        <h1>
                            <xsl:value-of select="pais"/>
                        </h1>

                        <table border = "1">
                        <tr>
                            <th>Nome</th>
                            <th>Posição</th>
                            <th>Pontos</th>
                            <th>Vitróias</th>
                            <th>Empates</th>
                            <th>Derrotas</th>
                            <th>Golos Marcados</th>
                            <th>Golos Sofridos</th>
                        </tr>
                        <xsl:for-each select="clube" >
                            <xsl:sort select="posicaoclube" data-type="number" />
                            <tr>
                                    <td>
                                        <xsl:value-of select="nomeclube"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="posicaoclube"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="pontos"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="vitorias"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="empates"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="derrotas"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="golosmarcados"/>
                                    </td>
                                    <td>
                                        <xsl:value-of select="golossofridos"/>
                                    </td>
                            </tr>
                         </xsl:for-each>
                           </table>
                    </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>